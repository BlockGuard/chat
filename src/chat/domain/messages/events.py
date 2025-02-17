from dataclasses import dataclass

from chat.domain.chats.chat_id import ChatId
from chat.domain.messages.message_id import MessageId
from chat.domain.shared.events import DomainEvent
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class MessageSent(DomainEvent):
    chat_id: ChatId
    sender_id: UserId
    message_id: MessageId
    content: str


@dataclass(frozen=True)
class MessageEdited(DomainEvent):
    chat_id: ChatId
    sender_id: UserId
    message_id: MessageId
    new_content: str


@dataclass(frozen=True)
class MessageDeleted(DomainEvent):
    chat_id: ChatId
    sender_id: UserId
    message_id: MessageId
