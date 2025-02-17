from abc import ABC, abstractmethod

from chat.domain.shared.entity import Entity


class Specification[T: Entity](ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool: ...
