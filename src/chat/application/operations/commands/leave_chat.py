from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.command import Command
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.chat_types import ChatType
from chat.domain.chat.repository import ChatRepository
from chat.domain.member.events import MemberLeft
from chat.domain.member.repository import MemberRepository
from chat.domain.member.roles import MemberRole
from chat.domain.member.service import RightsTransferService
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class LeaveChat(Command[None]):
    chat_id: ChatId
    user_id: UserId


class LeaveChatHandler(RequestHandler[LeaveChat, None]):
    def __init__(
        self,
        member_repository: MemberRepository,
        time_provider: TimeProvider,
        chat_repository: ChatRepository,
        rights_transfer_service: RightsTransferService,
    ) -> None:
        self._rights_transfer_service = rights_transfer_service
        self._member_repository = member_repository
        self._time_provider = time_provider
        self._chat_repository = chat_repository

    async def handle(self, request: LeaveChat) -> None:
        chat = await self._chat_repository.with_chat_id(chat_id=request.chat_id)

        if not chat:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="Chat not found"
            )

        if chat.chat_type == ChatType.PRIVATE:
            raise ApplicationError(
                error_type=ErrorType.PERMISSION_ERROR,
                message="Can't leave private chat",
            )

        member = await self._member_repository.with_chat_id_and_user_id(
            chat_id=request.chat_id, user_id=request.user_id
        )

        if not member:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="Member not found"
            )

        if member.role == MemberRole.OWNER:
            await self._rights_transfer_service.transfer_owner_rights(
                chat_id=request.chat_id,
                current_date=self._time_provider.provide_current(),
            )

        member.add_event(
            MemberLeft(
                member_id=request.user_id,
                chat_id=request.chat_id,
                event_date=self._time_provider.provide_current(),
            )
        )

        self._member_repository.delete(member)
