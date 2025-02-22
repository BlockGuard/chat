from abc import ABC, abstractmethod
from collections.abc import Iterable

from chat.domain.chats.chat_id import ChatId
from chat.domain.messages.message import Message
from chat.domain.messages.message_id import MessageId


class MessageRepository(ABC):
    @abstractmethod
    def add(self, message: Message) -> None: ...
    @abstractmethod
    def delete(self, message: Message) -> None: ...
    @abstractmethod
    async def with_message_id(
        self, message_id: MessageId
    ) -> Message | None: ...
    @abstractmethod
    async def with_chat_id(
        self, chat_id: ChatId
    ) -> Iterable[Message]: ...
