from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.command import Command
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.events import ChatDeleted
from chat.domain.chat.repository import ChatRepository
from chat.domain.member.repository import MemberRepository
from chat.domain.member.roles import MemberRole
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class DeleteChat(Command[None]):
    user_id: UserId
    chat_id: ChatId


class DeleteChatHandler(RequestHandler[DeleteChat, None]):
    def __init__(
        self,
        chat_repository: ChatRepository,
        member_repository: MemberRepository,
        time_provider: TimeProvider,
    ) -> None:
        self._chat_repository = chat_repository
        self._member_repository = member_repository
        self._time_provider = time_provider

    async def handle(self, request: DeleteChat) -> None:
        chat = await self._chat_repository.with_chat_id(chat_id=request.chat_id)

        if not chat:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="Chat not found"
            )

        member = await self._member_repository.with_chat_id_and_user_id(
            chat_id=request.chat_id, user_id=request.user_id
        )

        if not member:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="Member not found"
            )

        if member.role not in (MemberRole.ADMIN, MemberRole.OWNER):
            raise ApplicationError(
                error_type=ErrorType.PERMISSION_ERROR,
                message="You are not allowed to delete this chat",
            )

        chat.add_event(
            ChatDeleted(
                chat_id=request.chat_id,
                owner_id=chat.owner_id,
                event_date=self._time_provider.provide_current(),
            )
        )
        self._chat_repository.add(chat)
