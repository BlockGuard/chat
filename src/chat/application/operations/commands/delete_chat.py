from dataclasses import dataclass

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Command
from chat.application.ports.context import Context
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chats.chat_id import ChatId
from chat.domain.chats.chat_room import ChatRoom
from chat.domain.chats.events import ChatRoomDeleted
from chat.domain.chats.repository import ChatRepository
from chat.domain.chats.specification import (
    ChatIdentifiedSpecification,
)
from chat.domain.shared.specification import Specification


@dataclass(frozen=True)
class DeleteChat(Command[None]):
    chat_id: ChatId


class DeleteChatHandler(RequestHandler[DeleteChat, None]):
    def __init__(
        self,
        chat_repository: ChatRepository,
        time_provider: TimeProvider,
        context: Context,
    ) -> None:
        self._chat_repository = chat_repository
        self._time_provider = time_provider
        self._context = context

    async def handle(self, request: DeleteChat) -> None:
        specification = ChatIdentifiedSpecification(request.chat_id)
        current_user_id = await self._context.user_id()

        chat = await self._select(specification)

        if not chat:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Chat with id {request.chat_id} not found",
            )

        event = ChatRoomDeleted(
            chat_id=request.chat_id,
            event_date=self._time_provider.provide_current(),
        )

        chat.ensure_member_in_chat(current_user_id)
        chat.remove_members()
        chat.add_event(event)

        self._chat_repository.delete(chat)

    async def _select(
        self, specification: Specification[ChatRoom]
    ) -> ChatRoom | None:
        result = await self._chat_repository.load(specification)
        return result.first()
