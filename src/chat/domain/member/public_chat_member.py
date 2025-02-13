from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.events import (
    MemberRoleChanged,
    PublicChatMemberStatusChanged,
)
from chat.domain.member.member import Member
from chat.domain.member.roles import MemberRole
from chat.domain.member.statuses import MemberStatus
from chat.domain.message.events import PublicChatMessageSent
from chat.domain.message.message_id import MessageId
from chat.domain.message.public_chat_message import PublicChatMessage
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class PublicChatMember(Member):
    def __init__(
        self,
        entity_id: UserId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        chat_id: ChatId,
        status: MemberStatus,
        role: MemberRole,
        joined_at: datetime,
    ) -> None:
        Member.__init__(
            self=self,
            entity_id=entity_id,
            event_adder=event_adder,
            unit_of_work=unit_of_work,
            chat_id=chat_id,
            status=status,
            joined_at=joined_at,
        )

        self._role = role

    def send_message(
        self,
        message_id: MessageId,
        content: str,
        current_date: datetime,
    ) -> PublicChatMessage:
        self._ensure_can_send_message()

        message = PublicChatMessage(
            entity_id=message_id,
            event_adder=self._event_adder,
            unit_of_work=self._unit_of_work,
            owner_id=self.entity_id,
            chat_id=self.chat_id,
            content=content,
            created_at=current_date,
            updated_at=None,
        )
        event = PublicChatMessageSent(
            chat_id=self._chat_id,
            message_id=message_id,
            sender_id=self._entity_id,
            content=content,
            event_date=current_date,
        )
        message.add_event(event)
        message.mark_new()

        return message

    def edit_role(
        self, role: MemberRole, current_date: datetime
    ) -> None:
        self._role = role
        event = MemberRoleChanged(
            chat_id=self._chat_id,
            user_id=self._entity_id,
            role=role,
            event_date=current_date,
        )
        self.add_event(event)

    def edit_status(
        self, status: MemberStatus, current_date: datetime
    ) -> None:
        self._status = status
        event = PublicChatMemberStatusChanged(
            chat_id=self._chat_id,
            user_id=self._entity_id,
            status=status,
            event_date=current_date,
        )
        self.add_event(event)

    @property
    def role(self) -> MemberRole:
        return self._role
