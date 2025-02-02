from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.invitation.events import InvitationStatusChanged
from chat.domain.invitation.invitation_id import InvitationId
from chat.domain.invitation.statuses import InvitationStatus
from chat.domain.shared.entity import Entity
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class Invitation(Entity[InvitationId]):
    def __init__(
        self,
        entity_id: InvitationId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        sended_from: UserId,
        chat_id: ChatId,
        recipient_id: UserId,
        sended_at: datetime,
        expires_at: datetime,
        status: InvitationStatus = InvitationStatus.PENDING,
    ) -> None:
        super().__init__(entity_id, event_adder, unit_of_work)

        self._sended_from = sended_from
        self._chat_id = chat_id
        self._sended_at = sended_at
        self._expires_at = expires_at
        self._status = status
        self._recipient_id = recipient_id

    def change_status(self, status: InvitationStatus, current_date: datetime) -> None:
        self._status = status

        self.add_event(
            InvitationStatusChanged(
                chat_id=self._chat_id,
                invitation_id=self.entity_id,
                sender_id=self._sended_from,
                status=status,
                event_date=current_date,
            )
        )
        self.mark_dirty()

    @property
    def sended_from(self) -> UserId:
        return self._sended_from

    @property
    def chat_id(self) -> ChatId:
        return self._chat_id

    @property
    def sended_at(self) -> datetime:
        return self._sended_at

    @property
    def expires_at(self) -> datetime:
        return self._expires_at

    @property
    def status(self) -> InvitationStatus:
        return self._status

    @property
    def recipient_id(self) -> UserId:
        return self._recipient_id
