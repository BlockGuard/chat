from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.events import MemberRoleChanged, MemberStatusChanged
from chat.domain.member.roles import MemberRole
from chat.domain.member.statuses import MemberStatus
from chat.domain.message.message import Message
from chat.domain.message.message_id import MessageId
from chat.domain.shared.entity import Entity
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class Member(Entity[UserId]):
    def __init__(
        self,
        entity_id: UserId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        chat_id: ChatId,
        role: MemberRole = MemberRole.MEMBER,
        status: MemberStatus = MemberStatus.ACTIVE,
        joined_at: datetime,
    ) -> None:
        super().__init__(entity_id, event_adder, unit_of_work)

        self._chat_id = chat_id
        self._joined_at = joined_at
        self._role = role
        self._status = status

    def send_message(
        self, message_id: MessageId, content: str, current_date: datetime
    ) -> Message:
        message = self._create_message(message_id, content, current_date)
        return message

    def _create_message(
        self, message_id: MessageId, content: str, current_date: datetime
    ) -> Message:
        return Message(
            entity_id=message_id,
            event_adder=self._event_adder,
            unit_of_work=self._unit_of_work,
            owner_id=self._entity_id,
            chat_id=self._chat_id,
            content=content,
            created_at=current_date,
        )

    def change_role(self, role: MemberRole, current_date: datetime) -> None:
        self._role = role
        self.add_event(
            MemberRoleChanged(
                chat_id=self._chat_id,
                user_id=self._entity_id,
                role=role,
                event_date=current_date,
            )
        )

    def change_status(
        self, status: MemberStatus, current_date: datetime
    ) -> None:
        self._status = status
        self.add_event(
            MemberStatusChanged(
                chat_id=self._chat_id,
                user_id=self._entity_id,
                status=status,
                event_date=current_date,
            )
        )

    @property
    def chat_id(self) -> ChatId:
        return self._chat_id

    @property
    def joined_at(self) -> datetime:
        return self._joined_at

    @property
    def role(self) -> MemberRole:
        return self._role

    @property
    def status(self) -> MemberStatus:
        return self._status
