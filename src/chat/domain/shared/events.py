from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from chat.domain.shared.entity import Entity
from chat.domain.shared.event_id import EventId
from chat.domain.shared.markers import Notification


@dataclass(frozen=True, kw_only=True)
class DomainEvent[EntityT: Entity](Notification):
    event_date: datetime
    event_id: EventId | None = field(default=None, init=False)
    entity_type: type[EntityT] = field(init=False)

    @property
    def event_type(self) -> str:
        return type(self).__name__

    def set_event_id(self, event_id: EventId) -> None:
        if self.event_id:
            raise ValueError("Identifier already set")

        object.__setattr__(self, "event_id", event_id)


class DomainEventAdder(ABC):
    @abstractmethod
    def add_event(self, event: DomainEvent) -> None: ...
