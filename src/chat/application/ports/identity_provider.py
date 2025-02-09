from abc import ABC, abstractmethod

from chat.domain.shared.user_id import UserId


class IdentityProvider(ABC):
    @abstractmethod
    async def provide_current_user_id(self) -> UserId: ...
