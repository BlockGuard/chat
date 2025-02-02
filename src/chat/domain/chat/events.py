from dataclasses import dataclass

from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.chat_types import ChatType
from chat.domain.shared.events import DomainEvent
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class ChatCreated(DomainEvent):
    chat_id: ChatId
    owner_id: UserId
    title: str | None
    description: str | None
    chat_type: ChatType


@dataclass(frozen=True)
class ChatTitleChanged(DomainEvent):
    chat_id: ChatId
    owner_id: UserId
    title: str


@dataclass(frozen=True)
class ChatDescriptionChanged(DomainEvent):
    chat_id: ChatId
    owner_id: UserId
    description: str


@dataclass(frozen=True)
class ChatDeleted(DomainEvent):
    chat_id: ChatId
    owner_id: UserId
