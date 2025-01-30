from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.member_id import MemberId
from chat.domain.message.events import MessageContentEdited
from chat.domain.message.message_id import MessageId
from chat.domain.shared.entity import Entity
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork


class Message(Entity[MessageId]):
    def __init__(
        self,
        entity_id: MessageId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        owner_id: MemberId,
        chat_id: ChatId,
        content: str,
        created_at: datetime,
        updated_at: datetime | None = None,
    ) -> None:
        super().__init__(entity_id, event_adder, unit_of_work)

        self._owner_id = owner_id
        self._chat_id = chat_id
        self._content = content
        self._created_at = created_at
        self._updated_at = updated_at

    def change_content(self, content: str, current_time: datetime) -> None:
        self._content = content
        self._updated_at = current_time

        self.add_event(
            MessageContentEdited(
                message_id=self._entity_id,
                owner_id=self._owner_id,
                chat_id=self._chat_id,
                content=self._content,
                event_date=current_time,
            )
        )
        self.mark_dirty()

    @property
    def owner_id(self) -> MemberId:
        return self._owner_id

    @property
    def chat_id(self) -> ChatId:
        return self._chat_id

    @property
    def content(self) -> str:
        return self._content

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at
