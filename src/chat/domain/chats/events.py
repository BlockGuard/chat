from dataclasses import dataclass

from chat.domain.chats.chat_id import ChatId
from chat.domain.shared.events import DomainEvent


@dataclass(frozen=True)
class ChatRoomCreated(DomainEvent):
    chat_id: ChatId


@dataclass(frozen=True)
class ChatRoomDeleted(DomainEvent):
    chat_id: ChatId
