from dataclasses import dataclass

from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Command
from chat.application.ports.context import Context
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chats.chat_id import ChatId
from chat.domain.chats.factory import ChatFactory
from chat.domain.chats.repository import ChatRepository
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class StartMessaging(Command[ChatId]):
    companion_id: UserId


class StartMessagingHandler(RequestHandler[StartMessaging, ChatId]):
    def __init__(
        self,
        chat_repository: ChatRepository,
        chat_factory: ChatFactory,
        time_provider: TimeProvider,
        context: Context,
    ) -> None:
        self._chat_repository = chat_repository
        self._chat_factory = chat_factory
        self._time_provider = time_provider
        self._context = context

    async def handle(self, request: StartMessaging) -> ChatId:
        current_user_id = await self._context.user_id()
        chat = self._chat_factory.create_chat_room()

        chat.join_chat(
            member_id=current_user_id,
            current_date=self._time_provider.provide_current(),
        )
        chat.join_chat(
            member_id=request.companion_id,
            current_date=self._time_provider.provide_current(),
        )

        self._chat_repository.add(chat)

        return chat.entity_id
