from chat.domain.chat.chat_id import ChatId
from chat.domain.member.exceptions import (
    MemberAlreadyInChatError,
    MemberNotInChatError,
)
from chat.domain.member.member import Member
from chat.domain.shared.user_id import UserId


class MemberCollection[T: Member](set[T]):
    def __init__(self) -> None:
        set.__init__(self)

    def add(self, element: T) -> None:
        if element in self:
            raise MemberAlreadyInChatError(
                chat_id=element.chat_id, member_id=element.entity_id
            )
        self.add(element)

    def get(self, member_id: UserId, chat_id: ChatId) -> T:
        for member in self:
            if member.entity_id == member_id:
                return member

        raise MemberNotInChatError(
            chat_id=chat_id, member_id=member_id
        )

    def clear(self) -> None:
        for member in self:
            member.mark_deleted()
