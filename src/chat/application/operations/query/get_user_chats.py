from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.markers.query import Query
from chat.application.models.chat import ChatReadModel
from chat.application.models.pagination import Pagination
from chat.application.ports.chat_gateway import ChatGateway
from chat.application.ports.identity_provider import IdentityProvider


@dataclass(frozen=True)
class GetUserChats(Query[list[ChatReadModel]]):
    pagination: Pagination


class GetUserChatsHandler(RequestHandler[GetUserChats, list[ChatReadModel]]):
    def __init__(
        self,
        chat_gateway: ChatGateway,
        identity_provider: IdentityProvider,
    ) -> None:
        self._chat_gateway = chat_gateway
        self._identity_provider = identity_provider

    async def handle(self, request: GetUserChats) -> list[ChatReadModel]:
        current_user_id = await self._identity_provider.provide_current_user_id()
        chats = await self._chat_gateway.with_user_id(
            user_id=current_user_id, pagination=request.pagination
        )

        return chats
