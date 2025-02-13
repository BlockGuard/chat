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
class PrivateChatMessageSent(MessageSent): ...


@dataclass(frozen=True)
class PublicChatMessageSent(MessageSent): ...


@dataclass(frozen=True)
class MessageEdited(DomainEvent):
    chat_id: ChatId
    message_id: MessageId
    sender_id: UserId
    content: str


@dataclass(frozen=True)
class PrivateChatMessageEdited(MessageEdited): ...


@dataclass(frozen=True)
class PublicChatMessageEdited(MessageEdited): ...


@dataclass(frozen=True)
class MessageDeleted(DomainEvent):
    chat_id: ChatId
    message_id: MessageId
    sender_id: UserId


@dataclass(frozen=True)
class PrivateChatMessageDeleted(MessageDeleted): ...


@dataclass(frozen=True)
class PublicChatMessageDeleted(MessageDeleted): ...
