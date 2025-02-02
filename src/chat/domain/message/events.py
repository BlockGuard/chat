from dataclasses import dataclass

from chat.domain.chat.chat_id import ChatId
from chat.domain.message.message_id import MessageId
from chat.domain.shared.events import DomainEvent
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class MessageCreated(DomainEvent):
    message_id: MessageId
    owner_id: UserId
    chat_id: ChatId
    content: str


@dataclass(frozen=True)
class MessageContentEdited(DomainEvent):
    message_id: MessageId
    owner_id: UserId
    chat_id: ChatId
    content: str


@dataclass(frozen=True)
class MessageDeleted(DomainEvent):
    message_id: MessageId
    owner_id: UserId
    chat_id: ChatId
