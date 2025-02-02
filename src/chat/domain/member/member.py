from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.invitation.events import InvitationSent
from chat.domain.invitation.invitation import Invitation
from chat.domain.invitation.invitation_id import InvitationId
from chat.domain.member.events import MemberRoleChanged
from chat.domain.member.roles import MemberRole
from chat.domain.message.events import MessageCreated
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
        role: MemberRole,
        joined_at: datetime,
    ) -> None:
        super().__init__(entity_id, event_adder, unit_of_work)

        self._chat_id = chat_id
        self._joined_at = joined_at
        self._role = role

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

    def send_invitation(
        self,
        invitation_id: InvitationId,
        recipient_id: UserId,
        expires_at: datetime,
        current_date: datetime,
    ) -> Invitation:
        invitation = Invitation(
            entity_id=invitation_id,
            event_adder=self._event_adder,
            unit_of_work=self._unit_of_work,
            sended_from=self.entity_id,
            chat_id=self._chat_id,
            recipient_id=recipient_id,
            sended_at=current_date,
            expires_at=expires_at,
        )

        invitation.add_event(
            InvitationSent(
                recipient_id=recipient_id,
                chat_id=self._chat_id,
                invitation_id=invitation_id,
                sender_id=self.entity_id,
                expires_at=expires_at,
                event_date=current_date,
            )
        )

        return invitation

    def change_role(self, role: MemberRole, current_date: datetime) -> None:
        self._role = role

        self.add_event(
            MemberRoleChanged(
                member_id=self.entity_id,
                chat_id=self._chat_id,
                role=role,
                event_date=current_date,
            )
        )
        self.mark_dirty()

    @property
    def chat_id(self) -> ChatId:
        return self._chat_id

    @property
    def joined_at(self) -> datetime:
        return self._joined_at

    @property
    def role(self) -> MemberRole:
        return self._role
