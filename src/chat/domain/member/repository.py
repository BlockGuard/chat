from abc import ABC, abstractmethod

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.member import Member
from chat.domain.shared.user_id import UserId


class MemberRepository(ABC):
    @abstractmethod
    def delete(self, member: Member) -> None: ...
    @abstractmethod
    def delete_many(self, members: list[Member]) -> None: ...
    @abstractmethod
    async def with_chat_id(self, chat_id: ChatId) -> list[Member]: ...
    @abstractmethod
    async def with_chat_id_and_user_id(
        self, user_id: UserId, chat_id: ChatId
    ) -> Member | None: ...
    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> list[Member]: ...
