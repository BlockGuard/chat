from abc import ABC, abstractmethod

from chat.domain.chats.chat_room import ChatRoom
from chat.domain.shared.specification import Result, Specification


class ChatRepository(ABC):
    @abstractmethod
    def add(self, chat_room: ChatRoom) -> None: ...
    @abstractmethod
    def delete(self, chat_room: ChatRoom) -> None: ...
    @abstractmethod
    async def load(
        self, specification: Specification[ChatRoom]
    ) -> Result[ChatRoom]: ...
