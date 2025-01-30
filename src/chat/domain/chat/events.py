from dataclasses import dataclass

from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.owner_id import OwnerId
from chat.domain.shared.events import DomainEvent


@dataclass(frozen=True)
class ChatCreated(DomainEvent):
    chat_id: ChatId
    owner_id: OwnerId
    title: str
    description: str


@dataclass(frozen=True)
class ChatTitleChanged(DomainEvent):
    chat_id: ChatId
    owner_id: OwnerId
    title: str


@dataclass(frozen=True)
class ChatDescriptionChanged(DomainEvent):
    chat_id: ChatId
    owner_id: OwnerId
    description: str


@dataclass(frozen=True)
class ChatDeleted(DomainEvent):
    chat_id: ChatId
    owner_id: OwnerId
