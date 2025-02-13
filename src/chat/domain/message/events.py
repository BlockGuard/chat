from dataclasses import dataclass

from chat.domain.chat.chat_id import ChatId
from chat.domain.message.message import Message
from chat.domain.message.message_id import MessageId
from chat.domain.message.private_chat_message import (
    PrivateChatMessage,
)
from chat.domain.message.public_chat_message import PublicChatMessage
from chat.domain.shared.events import DomainEvent
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class MessageSent[MessageT: Message](DomainEvent[MessageT]):
    chat_id: ChatId
    message_id: MessageId
    sender_id: UserId
    content: str


@dataclass(frozen=True)
class PrivateChatMessageSent(MessageSent[PrivateChatMessage]): ...


@dataclass(frozen=True)
class PublicChatMessageSent(MessageSent[PublicChatMessage]): ...


@dataclass(frozen=True)
class MessageEdited[MessageT: Message](DomainEvent[MessageT]):
    chat_id: ChatId
    message_id: MessageId
    sender_id: UserId
    content: str


@dataclass(frozen=True)
class PrivateChatMessageEdited(MessageEdited[PrivateChatMessage]): ...


@dataclass(frozen=True)
class PublicChatMessageEdited(MessageEdited[PublicChatMessage]): ...


@dataclass(frozen=True)
class MessageDeleted[MessageT: Message](DomainEvent[MessageT]):
    chat_id: ChatId
    message_id: MessageId
    sender_id: UserId


@dataclass(frozen=True)
class PrivateChatMessageDeleted(
    MessageDeleted[PrivateChatMessage]
): ...


@dataclass(frozen=True)
class PublicChatMessageDeleted(MessageDeleted[PublicChatMessage]): ...
