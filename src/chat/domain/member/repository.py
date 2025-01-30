from abc import ABC, abstractmethod

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.member import Member
from chat.domain.member.member_id import MemberId


class MemberRepository(ABC):
    @abstractmethod
    def add(self, member: Member) -> None: ...
    @abstractmethod
    def delete(self, member: Member) -> None: ...
    @abstractmethod
    async def with_chat_id(self, chat_id: ChatId) -> list[Member]: ...
    @abstractmethod
    async def with_member_id(self, member_id: MemberId) -> Member | None: ...
