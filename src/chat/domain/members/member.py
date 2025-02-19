from datetime import datetime

from chat.domain.chats.chat_id import ChatId
from chat.domain.members.events import MemberStatusChanged
from chat.domain.members.exception import (
    BlockedMemberCantSendMessageError,
)
from chat.domain.members.statuses import Status
from chat.domain.messages.events import MessageSent
from chat.domain.messages.message import Message
from chat.domain.messages.message_id import MessageId
from chat.domain.reactions.reactions_collection import (
    ReactionsCollection,
)
from chat.domain.shared.entity import Entity
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class ChatMember(Entity[UserId]):
    def __init__(
        self,
        entity_id: UserId,
        unit_of_work: UnitOfWork,
        event_adder: DomainEventAdder,
        *,
        chat_id: ChatId,
        status: Status = Status.ACTIVE,
    ) -> None:
        Entity.__init__(self, entity_id, event_adder, unit_of_work)

        self._chat_id = chat_id
        self._status = status

    def send_message(
        self,
        message_id: MessageId,
        content: str,
        current_date: datetime,
    ) -> Message:
        self.ensure_active()
        message = Message(
            entity_id=message_id,
            unit_of_work=self._unit_of_work,
            event_adder=self._event_adder,
            sender_id=self._entity_id,
            chat_id=self._chat_id,
            text=content,
            sent_at=current_date,
            edited_at=None,
            reactions=ReactionsCollection(),
        )
        event = MessageSent(
            chat_id=self._chat_id,
            sender_id=self._entity_id,
            message_id=message_id,
            content=content,
            event_date=current_date,
        )
        message.add_event(event)

        return message

    def edit_status(
        self, status: Status, current_date: datetime
    ) -> None:
        self._status = status
        event = MemberStatusChanged(
            chat_id=self._chat_id,
            user_id=self._entity_id,
            status=status,
            event_date=current_date,
        )
        self.add_event(event)

    def ensure_active(self) -> None:
        if self._status != Status.ACTIVE:
            raise BlockedMemberCantSendMessageError

    @property
    def chat_id(self) -> ChatId:
        return self._chat_id

    @property
    def status(self) -> Status:
        return self._status
