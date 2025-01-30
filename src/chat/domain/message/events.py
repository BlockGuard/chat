from dataclasses import dataclass

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.member_id import MemberId
from chat.domain.message.message_id import MessageId
from chat.domain.shared.events import DomainEvent


@dataclass(frozen=True)
class MessageCreated(DomainEvent):
    message_id: MessageId
    owner_id: MemberId
    chat_id: ChatId
    content: str


@dataclass(frozen=True)
class MessageContentEdited(DomainEvent):
    message_id: MessageId
    owner_id: MemberId
    chat_id: ChatId
    content: str


@dataclass(frozen=True)
class MessageDeleted(DomainEvent):
    message_id: MessageId
    owner_id: MemberId
    chat_id: ChatId
