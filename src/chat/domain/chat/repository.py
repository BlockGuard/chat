from abc import ABC, abstractmethod

from chat.domain.chat.base_chat import BaseChat
from chat.domain.chat.chat_id import ChatId


class Result[ChatT: BaseChat](ABC):
    @abstractmethod
    async def with_chat_id(self, chat_id: ChatId) -> ChatT | None: ...


class ChatRepository(ABC):
    @abstractmethod
    def add(self, chat: BaseChat) -> None: ...
    @abstractmethod
    def delete(self, chat: BaseChat) -> None: ...
    @abstractmethod
    def select[ChatT: BaseChat](
        self, entity: type[ChatT]
    ) -> Result[ChatT]: ...
