from abc import ABC, abstractmethod

from chat.domain.chats.chat_id import ChatId
from chat.domain.chats.chat_room import ChatRoom


class ChatRepository(ABC):
    @abstractmethod
    def add(self, chat_room: ChatRoom) -> None: ...
    @abstractmethod
    def delete(self, chat_room: ChatRoom) -> None: ...
    @abstractmethod
    async def with_chat_id(
        self, chat_id: ChatId
    ) -> ChatRoom | None: ...
