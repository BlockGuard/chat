from abc import ABC, abstractmethod

from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.private_chat import PrivateChat
from chat.domain.chat.public_chat import PublicChat
from chat.domain.shared.user_id import UserId


class PrivateChatRepository(ABC):
    @abstractmethod
    def add(self, chat: PrivateChat) -> None: ...
    @abstractmethod
    def delete(self, chat: PrivateChat) -> None: ...
    @abstractmethod
    async def with_chat_id(self, chat_id: ChatId) -> PrivateChat | None: ...
    @abstractmethod
    async def with_owner_id(self, owner_id: UserId) -> list[PrivateChat]: ...


class PublicChatRepository(ABC):
    @abstractmethod
    def add(self, chat: PublicChat) -> None: ...
    @abstractmethod
    def delete(self, chat: PublicChat) -> None: ...
    @abstractmethod
    async def with_chat_id(self, chat_id: ChatId) -> PublicChat | None: ...
    @abstractmethod
    async def with_owner_id(self, owner_id: UserId) -> list[PublicChat]: ...
