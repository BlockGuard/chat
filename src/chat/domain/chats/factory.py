from abc import ABC, abstractmethod

from chat.domain.chats.chat_id import ChatId
from chat.domain.chats.chat_room import ChatRoom


class ChatFactory(ABC):
    @abstractmethod
    def create_chat_room(self, chat_id: ChatId) -> ChatRoom: ...
