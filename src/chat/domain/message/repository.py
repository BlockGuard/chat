from abc import ABC, abstractmethod

from chat.domain.chat.chat_id import ChatId
from chat.domain.message.message import Message
from chat.domain.message.message_id import MessageId
from chat.domain.shared.user_id import UserId


class MessageRepository(ABC):
    @abstractmethod
    def add(self, message: Message) -> None: ...
    @abstractmethod
    def delete(self, message: Message) -> None: ...
    @abstractmethod
    def delete_many(self, messages: list[Message]) -> None: ...
    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> list[Message]: ...
    @abstractmethod
    async def with_message_id(self, message_id: MessageId) -> Message | None: ...
    @abstractmethod
    async def with_chat_id(self, chat_id: ChatId) -> list[Message]: ...
