from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.markers.command import Command
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.factory import ChatFactory
from chat.domain.chat.repository import ChatRepository
from chat.domain.member.repository import MemberRepository
from chat.domain.member.roles import MemberRole
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class CreatePublicChat(Command[ChatId]):
    owner_id: UserId
    title: str
    description: str


class CreatePublicChatHandler(RequestHandler[CreatePublicChat, ChatId]):
    def __init__(
        self,
        chat_factory: ChatFactory,
        chat_repository: ChatRepository,
        member_repository: MemberRepository,
        time_provider: TimeProvider,
    ) -> None:
        self._chat_factory = chat_factory
        self._chat_repository = chat_repository
        self._member_repository = member_repository
        self._time_provider = time_provider

    async def handle(self, request: CreatePublicChat) -> ChatId:
        chat = await self._chat_factory.create_public_chat(
            owner_id=request.owner_id,
            title=request.title,
            description=request.description,
        )
        owner = chat.join_member(
            member_id=request.owner_id,
            current_date=self._time_provider.provide_current(),
            role=MemberRole.OWNER,
        )

        self._chat_repository.add(chat)
        self._member_repository.add(owner)

        return chat.entity_id
