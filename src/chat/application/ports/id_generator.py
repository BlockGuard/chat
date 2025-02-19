from abc import ABC, abstractmethod

from chat.domain.chats.chat_id import ChatId
from chat.domain.messages.message_id import MessageId
from chat.domain.reactions.reaction_id import ReactionId
from chat.domain.shared.event_id import EventId


class IdGenerator(ABC):
    @abstractmethod
    def generate_event_id(self) -> EventId: ...
    @abstractmethod
    def generate_chat_id(self) -> ChatId: ...
    @abstractmethod
    def generate_message_id(self) -> MessageId: ...
    @abstractmethod
    def generate_reaction_id(self) -> ReactionId: ...
