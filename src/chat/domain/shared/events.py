from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import get_args

from chat.domain.shared.entity import Entity
from chat.domain.shared.event_id import EventId
from chat.domain.shared.markers import Notification


@dataclass(frozen=True, kw_only=True)
class DomainEvent[EntityT: Entity](Notification):
    event_date: datetime
    event_id: EventId | None = field(default=None, init=False)
    entity_type: EntityT = field(init=False)

    @property
    def event_type(self) -> str:
        return type(self).__name__

    def set_event_id(self, event_id: EventId) -> None:
        if self.event_id:
            raise ValueError("Identifier already set")

        object.__setattr__(self, "event_id", event_id)

    def __post_init__(self) -> None:
        entity_type = get_args(self.__class__.__orig_class__)[0]  # type: ignore
        object.__setattr__(self, "entity_type", entity_type)


class DomainEventAdder(ABC):
    @abstractmethod
    def add_event(self, event: DomainEvent) -> None: ...
