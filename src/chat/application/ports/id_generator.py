from abc import ABC, abstractmethod

from chat.domain.chat.chat_id import ChatId
from chat.domain.invitation.invitation_id import InvitationId
from chat.domain.message.message_id import MessageId
from chat.domain.shared.event_id import EventId


class IdGenerator(ABC):
    @abstractmethod
    def generate_chat_id(self) -> ChatId: ...
    @abstractmethod
    def generate_invitation_id(self) -> InvitationId: ...
    @abstractmethod
    def generate_message_id(self) -> MessageId: ...
    @abstractmethod
    def generate_event_id(self) -> EventId: ...
