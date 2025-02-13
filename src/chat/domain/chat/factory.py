from abc import ABC, abstractmethod

from chat.domain.chat.private_chat import PrivateChat
from chat.domain.chat.public_chat import PublicChat
from chat.domain.shared.user_id import UserId


class ChatFactory(ABC):
    @abstractmethod
    async def create_public_chat(
        self,
        owner_id: UserId,
        title: str | None,
        description: str | None,
    ) -> PublicChat: ...
    @abstractmethod
    async def create_private_chat(
        self, owner_id: UserId
    ) -> PrivateChat: ...
