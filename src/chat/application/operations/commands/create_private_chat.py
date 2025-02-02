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
class CreatePrivateChat(Command[ChatId]):
    owner_id: UserId
    invited_user_id: UserId


class CreatePrivateChatHandler(
    RequestHandler[CreatePrivateChat, ChatId],
):
    def __init__(
        self,
        chat_repository: ChatRepository,
        chat_factory: ChatFactory,
        member_repository: MemberRepository,
        time_provider: TimeProvider,
    ) -> None:
        self._chat_factory = chat_factory
        self._chat_repository = chat_repository
        self._member_repository = member_repository
        self._time_provider = time_provider

    async def handle(self, request: CreatePrivateChat) -> ChatId:
        chat = await self._chat_factory.create_private_chat(request.owner_id)

        chat.join_member(
            member_id=request.owner_id,
            current_date=self._time_provider.provide_current(),
            role=MemberRole.OWNER,
        )

        chat.join_member(
            member_id=request.invited_user_id,
            current_date=self._time_provider.provide_current(),
            role=MemberRole.OWNER,
        )

        self._chat_repository.add(chat)

        return chat.entity_id
