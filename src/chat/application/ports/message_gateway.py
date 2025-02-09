from abc import ABC, abstractmethod

from chat.application.models.message import MessageReadModel
from chat.application.models.pagination import Pagination
from chat.domain.chat.chat_id import ChatId


class MessageGateway(ABC):
    @abstractmethod
    async def with_chat_id(
        self, chat_id: ChatId, pagination: Pagination
    ) -> list[MessageReadModel]: ...
