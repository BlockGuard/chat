from abc import ABC, abstractmethod

from chat.domain.chat.chat import Chat
from chat.domain.shared.user_id import UserId


class ChatFactory(ABC):
    @abstractmethod
    async def create_public_chat(
        self, owner_id: UserId, title: str, description: str
    ) -> Chat: ...
    @abstractmethod
    async def create_private_chat(self, owner_id: UserId) -> Chat: ...
