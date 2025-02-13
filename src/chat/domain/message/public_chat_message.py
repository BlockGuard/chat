from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.message.events import PublicChatMessageEdited
from chat.domain.message.message import Message
from chat.domain.message.message_id import MessageId
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class PublicChatMessage(Message):
    def __init__(
        self,
        entity_id: MessageId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        owner_id: UserId,
        chat_id: ChatId,
        content: str,
        created_at: datetime,
        updated_at: datetime | None,
    ) -> None:
        Message.__init__(
            self=self,
            entity_id=entity_id,
            event_adder=event_adder,
            unit_of_work=unit_of_work,
            owner_id=owner_id,
            chat_id=chat_id,
            content=content,
            created_at=created_at,
            updated_at=updated_at,
        )

    def change_content(
        self, content: str, current_date: datetime
    ) -> None:
        self._change_content(
            content=content, current_date=current_date
        )
        event = PublicChatMessageEdited(
            chat_id=self._chat_id,
            message_id=self._entity_id,
            sender_id=self._owner_id,
            content=content,
            event_date=current_date,
        )
        self.add_event(event)
