from abc import abstractmethod
from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.exceptions import (
    MutedMemberCantSendMessageError,
)
from chat.domain.member.statuses import MemberStatus
from chat.domain.message.message import Message
from chat.domain.message.message_id import MessageId
from chat.domain.shared.entity import Entity
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class Member[MessageT: Message](Entity[UserId]):
    def __init__(
        self,
        entity_id: UserId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        chat_id: ChatId,
        status: MemberStatus,
        joined_at: datetime,
    ) -> None:
        Entity.__init__(
            self=self,
            entity_id=entity_id,
            event_adder=event_adder,
            unit_of_work=unit_of_work,
        )

        self._chat_id = chat_id
        self._joined_at = joined_at
        self._status = status

    @abstractmethod
    def send_message(
        self,
        message_id: MessageId,
        content: str,
        current_date: datetime,
    ) -> MessageT: ...

    @abstractmethod
    def edit_status(
        self, status: MemberStatus, current_date: datetime
    ) -> None: ...

    def _ensure_can_send_message(self) -> None:
        if self.status == MemberStatus.MUTED:
            raise MutedMemberCantSendMessageError(
                chat_id=self.chat_id, member_id=self.entity_id
            )

    @property
    def chat_id(self) -> ChatId:
        return self._chat_id

    @property
    def joined_at(self) -> datetime:
        return self._joined_at

    @property
    def status(self) -> MemberStatus:
        return self._status
