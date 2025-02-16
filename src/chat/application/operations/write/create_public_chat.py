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
class CreatePublicChat(Command[ChatId]):
    title: str | None
    description: str | None
    invited_members: set[UserId]


class CreatePublicChatHandler(
    RequestHandler[CreatePublicChat, ChatId]
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

    async def handle(self, request: CreatePublicChat) -> ChatId:
        current_user_id = await self._context.user_id()
        public_chat = self._factory.create_public_chat(
            title=request.title, description=request.description
        )

        public_chat.join(
            member_id=current_user_id,
            current_date=self._time_provider.provide_current(),
        )

        for invited_member in request.invited_members:
            public_chat.join(
                member_id=invited_member,
                current_date=self._time_provider.provide_current(),
            )

        self._repository.add(public_chat)

        return public_chat.entity_id
