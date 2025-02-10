from dataclasses import dataclass

from chat.domain.chat.chat_id import ChatId
from chat.domain.shared.events import DomainEvent


@dataclass(frozen=True)
class PublicChatCreated(DomainEvent):
    chat_id: ChatId
    title: str | None
    description: str | None


@dataclass(frozen=True)
class PublicChatDescriptionEdited(DomainEvent):
    chat_id: ChatId
    description: str | None


@dataclass(frozen=True)
class PublicChatTitleEdited(DomainEvent):
    chat_id: ChatId
    title: str | None


@dataclass(frozen=True)
class PublicChatDeleted(DomainEvent):
    chat_id: ChatId
