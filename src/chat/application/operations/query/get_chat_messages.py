from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.query import Query
from chat.application.models.message import MessageReadModel
from chat.application.models.pagination import Pagination
from chat.application.ports.chat_gateway import ChatGateway
from chat.application.ports.identity_provider import IdentityProvider
from chat.application.ports.message_gateway import MessageGateway
from chat.domain.chat.chat_id import ChatId


@dataclass(frozen=True)
class GetChatMessages(Query[list[MessageReadModel]]):
    chat_id: ChatId
    pagintation: Pagination


class GetChatMessagesHandler(
    RequestHandler[GetChatMessages, list[MessageReadModel]]
):
    def __init__(
        self,
        message_gateway: MessageGateway,
        chat_gateway: ChatGateway,
        identity_provider: IdentityProvider,
    ) -> None:
        self._message_gateway = message_gateway
        self._identity_provider = identity_provider
        self._chat_gateway = chat_gateway

    async def handle(self, request: GetChatMessages) -> list[MessageReadModel]:
        current_user_id = await self._identity_provider.provide_current_user_id()
        chat = await self._chat_gateway.with_chat_id(chat_id=request.chat_id)

        if not chat:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Chat with id {request.chat_id} not found",
            )
        if not chat.ensure_is_member(current_user_id):
            raise ApplicationError(
                error_type=ErrorType.FORBIDDEN,
                message="You are not a member of this chat",
            )

        messages = await self._message_gateway.with_chat_id(
            chat_id=request.chat_id, pagination=request.pagintation
        )

        return messages
