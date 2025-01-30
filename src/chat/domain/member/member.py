from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.member_id import MemberId
from chat.domain.message.events import MessageCreated
from chat.domain.message.message import Message
from chat.domain.message.message_id import MessageId
from chat.domain.shared.entity import Entity
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork


class Member(Entity[MemberId]):
    def __init__(
        self,
        entity_id: MemberId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        chat_id: ChatId,
        joined_at: datetime,
    ) -> None:
        super().__init__(entity_id, event_adder, unit_of_work)

        self._chat_id = chat_id
        self._joined_at = joined_at

    def send_message(
        self, message_id: MessageId, content: str, current_date: datetime
    ) -> Message:
        message = Message(
            entity_id=message_id,
            event_adder=self._event_adder,
            unit_of_work=self._unit_of_work,
            owner_id=self.entity_id,
            chat_id=self._chat_id,
            content=content,
            created_at=current_date,
        )

        message.add_event(
            MessageCreated(
                message_id=message_id,
                owner_id=self.entity_id,
                chat_id=self._chat_id,
                content=content,
                event_date=current_date,
            )
        )
        return message

    @property
    def chat_id(self) -> ChatId:
        return self._chat_id

    @property
    def joined_at(self) -> datetime:
        return self._joined_at
