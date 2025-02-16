from dataclasses import dataclass

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Command
from chat.application.ports.context import Context
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.public_chat import PublicChat
from chat.domain.chat.repository import ChatRepository


@dataclass(frozen=True)
class LeaveChat(Command[None]):
    chat_id: ChatId


class LeaveChatHandler(RequestHandler[LeaveChat, None]):
    def __init__(
        self,
        repository: ChatRepository,
        time_provider: TimeProvider,
        context: Context,
    ) -> None:
        self._repository = repository
        self._time_provider = time_provider
        self._context = context

    async def handle(self, request: LeaveChat) -> None:
        current_user_id = await self._context.user_id()
        selected_chat = self._repository.select(PublicChat)
        public_chat = await selected_chat.with_chat_id(
            request.chat_id
        )

        if not public_chat:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message="Chat not found",
            )

        public_chat.leave(
            member_id=current_user_id,
            current_date=self._time_provider.provide_current(),
        )
