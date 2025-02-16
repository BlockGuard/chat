from dataclasses import dataclass

from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Command
from chat.application.ports.context import Context
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.factory import ChatFactory
from chat.domain.chat.repository import ChatRepository
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class CreatePrivateChat(Command[ChatId]):
    companion_id: UserId


class CreatePrivateChatHandler(
    RequestHandler[CreatePrivateChat, ChatId]
):
    def __init__(
        self,
        context: Context,
        factory: ChatFactory,
        repository: ChatRepository,
        time_provider: TimeProvider,
    ) -> None:
        self._context = context
        self._factory = factory
        self._repository = repository
        self._time_provider = time_provider

    async def handle(self, request: CreatePrivateChat) -> ChatId:
        current_user_id = await self._context.user_id()
        private_chat = self._factory.create_private_chat()

        private_chat.join(
            member_id=current_user_id,
            current_date=self._time_provider.provide_current(),
        )
        private_chat.join(
            member_id=request.companion_id,
            current_date=self._time_provider.provide_current(),
        )

        self._repository.add(private_chat)

        return private_chat.entity_id
