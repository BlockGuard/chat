from dataclasses import dataclass

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Query
from chat.application.models.chat import ChatReadModel
from chat.application.ports.chat_gateway import ChatGateway
from chat.application.ports.context import Context
from chat.domain.chats.chat_id import ChatId


@dataclass(frozen=True)
class GetChat(Query[ChatReadModel]):
    chat_id: ChatId


class GetMyChatsHandler(RequestHandler[GetChat, ChatReadModel]):
    def __init__(
        self, context: Context, chat_gateway: ChatGateway
    ) -> None:
        self._chat_gateway = chat_gateway
        self._context = context

    async def handle(self, request: GetChat) -> ChatReadModel:
        current_user_id = await self._context.user_id()

        chat = await self._chat_gateway.with_chat_id(request.chat_id)

        if not chat:
            raise ApplicationError(
                message="Chat not found",
                error_type=ErrorType.NOT_FOUND,
            )

        chat.ensure_member(current_user_id)

        return chat
