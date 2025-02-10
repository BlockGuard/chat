from abc import ABC, abstractmethod

from chat.domain.shared.entity import Entity
from chat.infrastructure.persistence.data_mapper import DataMapper


class DataMappersRegistry(ABC):
    @abstractmethod
    def get_mapper(self, entity: type[Entity]) -> DataMapper: ...
