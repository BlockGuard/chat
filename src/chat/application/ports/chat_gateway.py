from abc import ABC, abstractmethod

from chat.application.models.chat import ChatReadModel
from chat.application.models.pagination import Pagination
from chat.domain.chat.chat_id import ChatId
from chat.domain.shared.user_id import UserId


class ChatGateway(ABC):
    @abstractmethod
    async def with_chat_id(self, chat_id: ChatId) -> ChatReadModel | None: ...
    @abstractmethod
    async def with_user_id(
        self, user_id: UserId, pagination: Pagination
    ) -> list[ChatReadModel]: ...
