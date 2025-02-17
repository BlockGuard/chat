from abc import ABC, abstractmethod
from collections.abc import Iterable

from chat.domain.messages.message import Message
from chat.domain.shared.specification import Specification


class Result[T: Message](ABC):
    @abstractmethod
    def first(self) -> T: ...
    @abstractmethod
    def all(self) -> Iterable[T]: ...


class MessageRepository(ABC):
    @abstractmethod
    def add(self, message: Message) -> None: ...
    @abstractmethod
    def delete(self, message: Message) -> None: ...
    @abstractmethod
    def load[T: Message](
        self, specification: Specification[T]
    ) -> Result[T]: ...
