from abc import ABC, abstractmethod

from chat.domain.chat.chat import Chat
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.owner_id import OwnerId


class ChatRepository(ABC):
    @abstractmethod
    def add(self, chat: Chat) -> None: ...
    @abstractmethod
    def delete(self, chat: Chat) -> None: ...
    @abstractmethod
    async def with_chat_id(self, chat_id: ChatId) -> Chat | None: ...
    @abstractmethod
    async def with_owner_id(self, owner_id: OwnerId) -> list[Chat]: ...
