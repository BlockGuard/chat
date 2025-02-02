from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.command import Command
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.repository import ChatRepository
from chat.domain.invitation.invitation_id import InvitationId
from chat.domain.invitation.repository import InvitationRepository
from chat.domain.invitation.statuses import InvitationStatus
from chat.domain.member.repository import MemberRepository
from chat.domain.member.roles import MemberRole
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class AcceptChatInvitation(Command[None]):
    user_id: UserId
    invitation_id: InvitationId


class AcceptChatInvitationHandler(RequestHandler[AcceptChatInvitation, None]):
    def __init__(
        self,
        time_provider: TimeProvider,
        chat_repository: ChatRepository,
        member_repository: MemberRepository,
        invitation_repository: InvitationRepository,
    ) -> None:
        self._chat_repository = chat_repository
        self._time_provider = time_provider
        self._member_repository = member_repository
        self._invitation_repository = invitation_repository

    async def handle(self, request: AcceptChatInvitation) -> None:
        invitation = await self._invitation_repository.with_invitation_id(
            invitation_id=request.invitation_id
        )

        if not invitation:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="Invitation not found"
            )

        if invitation.expires_at < self._time_provider.provide_current():
            raise ApplicationError(
                error_type=ErrorType.BAD_REQUEST, message="Invitation expired"
            )

        await self._ensure_user_is_not_member_of_chat(
            chat_id=invitation.chat_id, user_id=invitation.recipient_id
        )

        if invitation.status != InvitationStatus.PENDING:
            raise ApplicationError(
                error_type=ErrorType.BAD_REQUEST,
                message="Invitation is not pending",
            )

        chat = await self._chat_repository.with_chat_id(chat_id=invitation.chat_id)

        if not chat:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="Chat not found"
            )

        member = chat.join_member(
            member_id=invitation.recipient_id,
            current_date=self._time_provider.provide_current(),
            role=MemberRole.MEMBER,
        )

        invitation.change_status(
            status=InvitationStatus.ACCEPTED,
            current_date=self._time_provider.provide_current(),
        )

        self._member_repository.add(member)

    async def _ensure_user_is_not_member_of_chat(
        self, chat_id: ChatId, user_id: UserId
    ) -> None:
        member = await self._member_repository.with_chat_id_and_user_id(
            chat_id=chat_id, user_id=user_id
        )

        if member:
            raise ApplicationError(
                error_type=ErrorType.BAD_REQUEST,
                message="User is already member of chat",
            )
