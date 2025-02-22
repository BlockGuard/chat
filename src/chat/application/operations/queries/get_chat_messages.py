from collections.abc import Iterable
from dataclasses import dataclass

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Query
from chat.application.models.message import MessageReadModel
from chat.application.models.pagination import Pagination
from chat.application.ports.chat_gateway import ChatGateway
from chat.application.ports.context import Context
from chat.application.ports.message_gateway import MessageGateway
from chat.domain.chats.chat_id import ChatId


@dataclass(frozen=True)
class GetChatMessages(Query[Iterable[MessageReadModel]]):
    chat_id: ChatId
    pagination: Pagination


class GetMyChatsHandler(
    RequestHandler[GetChatMessages, Iterable[MessageReadModel]]
):
    def __init__(
        self,
        context: Context,
        chat_gateway: ChatGateway,
        message_gateway: MessageGateway,
    ) -> None:
        self._chat_gateway = chat_gateway
        self._context = context
        self._message_gateway = message_gateway

    async def handle(
        self, request: GetChatMessages
    ) -> Iterable[MessageReadModel]:
        current_user_id = await self._context.user_id()

        chat = await self._chat_gateway.with_chat_id(request.chat_id)

        if not chat:
            raise ApplicationError(
                message="Chat not found",
                error_type=ErrorType.NOT_FOUND,
            )

        chat.ensure_member(current_user_id)

        messages = await self._message_gateway.with_chat_id(
            chat_id=request.chat_id, pagination=request.pagination
        )

        return messages
