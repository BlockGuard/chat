from dataclasses import dataclass
from datetime import datetime

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.command import Command
from chat.application.ports.id_generator import IdGenerator
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.chat_types import ChatType
from chat.domain.chat.repository import ChatRepository
from chat.domain.invitation.invitation_id import InvitationId
from chat.domain.invitation.repository import InvitationRepository
from chat.domain.member.repository import MemberRepository
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class SendInvitation(Command[InvitationId]):
    user_id: UserId
    chat_id: ChatId
    recipient_id: UserId
    expiration_date: datetime


class SendInvitationHandler(RequestHandler[SendInvitation, InvitationId]):
    def __init__(
        self,
        invitation_repository: InvitationRepository,
        member_repository: MemberRepository,
        time_provider: TimeProvider,
        id_generator: IdGenerator,
        chat_repository: ChatRepository,
    ) -> None:
        self._invitation_repository = invitation_repository
        self._member_repository = member_repository
        self._time_provider = time_provider
        self._id_generator = id_generator
        self._chat_repository = chat_repository

    async def handle(self, request: SendInvitation) -> InvitationId:
        chat = await self._chat_repository.with_chat_id(chat_id=request.chat_id)

        if not chat:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="Chat not found"
            )

        if chat.chat_type == ChatType.PRIVATE:
            raise ApplicationError(
                error_type=ErrorType.CONFLICT_ERROR,
                message="You cannot send invitations to private chats",
            )

        await self._ensure_recipient_is_not_member(
            chat_id=request.chat_id, recipient_id=request.recipient_id
        )

        sender = await self._member_repository.with_chat_id_and_user_id(
            user_id=request.user_id, chat_id=request.chat_id
        )

        if not sender:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message="You are not a part of this chat",
            )

        invitation = sender.send_invitation(
            invitation_id=self._id_generator.generate_invitation_id(),
            current_date=self._time_provider.provide_current(),
            expires_at=request.expiration_date,
            recipient_id=request.recipient_id,
        )
        self._invitation_repository.add(invitation)

        return invitation.entity_id

    async def _ensure_recipient_is_not_member(
        self, chat_id: ChatId, recipient_id: UserId
    ) -> None:
        member = await self._member_repository.with_chat_id_and_user_id(
            user_id=recipient_id, chat_id=chat_id
        )

        if member:
            raise ApplicationError(
                error_type=ErrorType.CONFLICT_ERROR,
                message="Recipient is already a member of this chat",
            )
