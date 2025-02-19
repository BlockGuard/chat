from abc import ABC, abstractmethod

from chat.domain.messages.message import Message
from chat.domain.shared.specification import Result, Specification


class MessageRepository(ABC):
    @abstractmethod
    def add(self, message: Message) -> None: ...
    @abstractmethod
    def delete(self, message: Message) -> None: ...
    @abstractmethod
    async def load(
        self, specification: Specification[Message]
    ) -> Result[Message]: ...
