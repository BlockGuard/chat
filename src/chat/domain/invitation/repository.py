from abc import ABC, abstractmethod

from chat.domain.chat.chat_id import ChatId
from chat.domain.invitation.invitation import Invitation
from chat.domain.invitation.invitation_id import InvitationId


class InvitationRepository(ABC):
    @abstractmethod
    def add(self, invitation: Invitation) -> None: ...
    @abstractmethod
    def delete(self, invitation: Invitation) -> None: ...
    @abstractmethod
    async def with_chat_id(self, chat_id: ChatId) -> list[Invitation]: ...
    @abstractmethod
    async def with_invitation_id(
        self, invitation_id: InvitationId
    ) -> Invitation | None: ...
