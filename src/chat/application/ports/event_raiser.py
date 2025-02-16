from abc import ABC, abstractmethod
from collections.abc import Iterable

from chat.domain.shared.events import DomainEvent


class DomainEventsRaiser(ABC):
    @abstractmethod
    def raise_events(self) -> Iterable[DomainEvent]: ...
