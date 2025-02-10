from abc import ABC, abstractmethod

from chat.domain.chat.public_chat import PublicChat
from chat.domain.shared.user_id import UserId


class ChatFactory(ABC):
    @abstractmethod
    async def create_public_chat(
        self,
        owner_id: UserId,
        title: str | None = None,
        description: str | None = None,
    ) -> PublicChat: ...
