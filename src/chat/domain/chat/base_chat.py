from abc import abstractmethod
from datetime import datetime
from typing import TypeVar

from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.chat_types import ChatType
from chat.domain.member.member import Member
from chat.domain.member.member_collection import MemberCollection
from chat.domain.member.statuses import MemberStatus
from chat.domain.message.message import Message
from chat.domain.message.message_id import MessageId
from chat.domain.shared.entity import Entity
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId

MemberT = TypeVar("MemberT", bound=Member)


class BaseChat[MemberT: Member](Entity[ChatId]):
    def __init__(
        self,
        entity_id: ChatId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        created_at: datetime,
        chat_type: ChatType,
        members: MemberCollection[MemberT],
    ) -> None:
        Entity.__init__(
            self=self,
            entity_id=entity_id,
            event_adder=event_adder,
            unit_of_work=unit_of_work,
        )

        self._created_at = created_at
        self._chat_type = chat_type
        self._members = members

    @abstractmethod
    def join(
        self,
        member_id: UserId,
        current_date: datetime,
    ) -> None: ...

    @abstractmethod
    def send_message(
        self,
        sender_id: UserId,
        message_id: MessageId,
        content: str,
        current_date: datetime,
    ) -> Message: ...

    def edit_member_status(
        self,
        member_id: UserId,
        status: MemberStatus,
        current_date: datetime,
        editor_id: UserId,
    ) -> None:
        self._members.get(
            member_id=editor_id, chat_id=self._entity_id
        )
        member = self._members.get(
            member_id=member_id, chat_id=self._entity_id
        )

        member.edit_status(status=status, current_date=current_date)
        member.mark_dirty()

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def chat_type(self) -> ChatType:
        return self._chat_type

    @property
    def members(self) -> set[MemberT]:
        return self._members
