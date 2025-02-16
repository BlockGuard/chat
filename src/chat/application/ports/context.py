from abc import ABC, abstractmethod

from chat.domain.shared.user_id import UserId


class Context(ABC):
    @abstractmethod
    async def user_id(self) -> UserId: ...
