from dataclasses import dataclass

from chat.domain.chat.base_chat import BaseChat
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.private_chat import PrivateChat
from chat.domain.chat.public_chat import PublicChat
from chat.domain.shared.events import DomainEvent


@dataclass(frozen=True)
class ChatCreated[ChatT: BaseChat](DomainEvent[ChatT]):
    chat_id: ChatId


@dataclass(frozen=True)
class PublicChatCreated(ChatCreated[PublicChat]):
    title: str | None
    description: str | None


@dataclass(frozen=True)
class PrivateChatCreated(ChatCreated[PrivateChat]): ...


@dataclass(frozen=True)
class PublicChatDescriptionEdited(DomainEvent[PublicChat]):
    chat_id: ChatId
    description: str | None


@dataclass(frozen=True)
class PublicChatTitleEdited(DomainEvent[PublicChat]):
    chat_id: ChatId
    title: str | None


@dataclass(frozen=True)
class ChatDeleted[ChatT: BaseChat](DomainEvent[ChatT]):
    chat_id: ChatId


@dataclass(frozen=True)
class PublicChatDeleted(ChatDeleted[PublicChat]): ...


@dataclass(frozen=True)
class PrivateChatDeleted(ChatDeleted[PrivateChat]): ...
