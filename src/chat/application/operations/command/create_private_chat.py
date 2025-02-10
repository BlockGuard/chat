from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.markers.command import Command
from chat.application.ports.identity_provider import IdentityProvider
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.factory import ChatFactory
from chat.domain.chat.repository import PrivateChatRepository
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class CreatePrivateChat(Command[ChatId]):
    companion_id: UserId


class CreatePrivateChatHandler(RequestHandler[CreatePrivateChat, ChatId]):
    def __init__(
        self,
        chat_factory: ChatFactory,
        time_provider: TimeProvider,
        private_chat_repository: PrivateChatRepository,
        identity_provider: IdentityProvider,
    ) -> None:
        self._chat_factory = chat_factory
        self._time_provider = time_provider
        self._private_chat_repository = private_chat_repository
        self._identity_provider = identity_provider

    async def handle(self, request: CreatePrivateChat) -> ChatId:
        current_user_id = await self._identity_provider.provide_current_user_id()
        private_chat = await self._chat_factory.create_private_chat(
            owner_id=current_user_id,
        )

        private_chat.join_private_chat(
            member_id=request.companion_id,
            current_date=self._time_provider.provide_current(),
        )

        private_chat.join_private_chat(
            member_id=current_user_id,
            current_date=self._time_provider.provide_current(),
        )

        self._private_chat_repository.add(chat=private_chat)

        return private_chat.entity_id
