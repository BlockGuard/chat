from abc import ABC, abstractmethod
from collections.abc import Iterable

from chat.domain.shared.entity import Entity


class Result[T: Entity](ABC):
    @abstractmethod
    def first(self) -> T: ...
    @abstractmethod
    def all(self) -> Iterable[T]: ...


class Specification[T: Entity](ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool: ...
