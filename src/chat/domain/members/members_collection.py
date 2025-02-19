from chat.domain.members.exception import (
    MemberAlreadyInChatError,
    MemberNotInChatError,
)
from chat.domain.members.member import ChatMember
from chat.domain.shared.user_id import UserId


class MemberCollection(set[ChatMember]):
    def __init__(self) -> None:
        set.__init__(self)

    def add(self, element: ChatMember) -> None:
        if element in self:
            raise MemberAlreadyInChatError

        self.add(element)

    def get(self, member_id: UserId) -> ChatMember:
        for member in self:
            if member.entity_id == member_id:
                return member

        raise MemberNotInChatError

    def clear(self) -> None:
        for member in self:
            member.mark_deleted()

        self.clear()

    def count(self) -> int:
        return len(self)
