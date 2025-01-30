from abc import ABC, abstractmethod

from chat.domain.chat.chat import Chat
from chat.domain.chat.owner_id import OwnerId


class ChatFactory(ABC):
    @abstractmethod
    def create(
        self, owner_id: OwnerId, title: str, description: str
    ) -> Chat: ...
