from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.markers.command import Command
from chat.application.ports.identity_provider import IdentityProvider
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.factory import ChatFactory
from chat.domain.chat.repository import PublicChatRepository
from chat.domain.member.roles import MemberRole


@dataclass(frozen=True)
class CreatePublicChat(Command[ChatId]):
    title: str | None
    description: str | None


class CreatePublicChatHandler(RequestHandler[CreatePublicChat, ChatId]):
    def __init__(
        self,
        chat_factory: ChatFactory,
        time_provider: TimeProvider,
        public_chat_repository: PublicChatRepository,
        identity_provider: IdentityProvider,
    ) -> None:
        self._chat_factory = chat_factory
        self._time_provider = time_provider
        self._public_chat_repository = public_chat_repository
        self._identity_provider = identity_provider

    async def handle(self, request: CreatePublicChat) -> ChatId:
        current_user_id = await self._identity_provider.provide_current_user_id()
        public_chat = await self._chat_factory.create_public_chat(
            owner_id=current_user_id,
            title=request.title,
            description=request.description,
        )

        public_chat.join_public_chat(
            member_id=current_user_id,
            current_date=self._time_provider.provide_current(),
            role=MemberRole.OWNER,
        )

        self._public_chat_repository.add(chat=public_chat)

        return public_chat.entity_id
