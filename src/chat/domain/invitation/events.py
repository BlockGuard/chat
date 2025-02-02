from dataclasses import dataclass
from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.invitation.invitation_id import InvitationId
from chat.domain.invitation.statuses import InvitationStatus
from chat.domain.shared.events import DomainEvent
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class InvitationSent(DomainEvent):
    chat_id: ChatId
    invitation_id: InvitationId
    sender_id: UserId
    recipient_id: UserId
    expires_at: datetime


@dataclass(frozen=True)
class InvitationStatusChanged(DomainEvent):
    chat_id: ChatId
    invitation_id: InvitationId
    sender_id: UserId
    status: InvitationStatus
