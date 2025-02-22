from abc import ABC, abstractmethod
from collections.abc import Iterable

from chat.application.models.message import MessageReadModel
from chat.application.models.pagination import Pagination
from chat.domain.chats.chat_id import ChatId


class MessageGateway(ABC):
    @abstractmethod
    async def with_chat_id(
        self, chat_id: ChatId, pagination: Pagination
    ) -> Iterable[MessageReadModel]: ...
