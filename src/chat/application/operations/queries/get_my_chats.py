from collections.abc import Iterable
from dataclasses import dataclass

from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Query
from chat.application.models.chat import ChatReadModel
from chat.application.models.pagination import Pagination
from chat.application.ports.chat_gateway import ChatGateway
from chat.application.ports.context import Context


@dataclass(frozen=True)
class GetMyChats(Query[Iterable[ChatReadModel]]):
    pagination: Pagination


class GetMyChatsHandler(
    RequestHandler[GetMyChats, Iterable[ChatReadModel]]
):
    def __init__(
        self, context: Context, chat_gateway: ChatGateway
    ) -> None:
        self._chat_gateway = chat_gateway
        self._context = context

    async def handle(
        self, request: GetMyChats
    ) -> Iterable[ChatReadModel]:
        current_user_id = await self._context.user_id()

        chats = await self._chat_gateway.with_user_id(
            user_id=current_user_id, pagination=request.pagination
        )

        return chats
