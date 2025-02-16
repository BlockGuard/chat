from abc import ABC, abstractmethod

from chat.domain.chat.private_chat import PrivateChat
from chat.domain.chat.public_chat import PublicChat


class ChatFactory(ABC):
    @abstractmethod
    def create_public_chat(
        self,
        title: str | None,
        description: str | None,
    ) -> PublicChat: ...
    @abstractmethod
    def create_private_chat(self) -> PrivateChat: ...
