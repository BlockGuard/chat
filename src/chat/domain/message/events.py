from dataclasses import dataclass

from chat.domain.chat.chat_id import ChatId
from chat.domain.message.message_id import MessageId
from chat.domain.shared.events import DomainEvent
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class MessageSent(DomainEvent):
    chat_id: ChatId
    message_id: MessageId
    sender_id: UserId
    content: str


@dataclass(frozen=True)
class MessageEdited(DomainEvent):
    chat_id: ChatId
    message_id: MessageId
    sender_id: UserId
    content: str


@dataclass(frozen=True)
class MessageDeleted(DomainEvent):
    chat_id: ChatId
    message_id: MessageId
    sender_id: UserId
