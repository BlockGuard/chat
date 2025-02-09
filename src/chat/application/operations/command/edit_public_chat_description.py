from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.command import Command
from chat.application.ports.identity_provider import IdentityProvider
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.repository import PublicChatRepository


@dataclass(frozen=True)
class EditPublicChatDescription(Command[None]):
    chat_id: ChatId
    new_description: str | None


class EditPublicChatDescriptionHandler(
    RequestHandler[EditPublicChatDescription, None]
):
    def __init__(
        self,
        time_provider: TimeProvider,
        public_chat_repository: PublicChatRepository,
        identity_provider: IdentityProvider,
    ) -> None:
        self._time_provider = time_provider
        self._public_chat_repository = public_chat_repository
        self._identity_provider = identity_provider

    async def handle(self, request: EditPublicChatDescription) -> None:
        current_user_id = await self._identity_provider.provide_current_user_id()
        public_chat = await self._public_chat_repository.with_chat_id(
            chat_id=request.chat_id
        )

        if not public_chat:
            raise ApplicationError(
                message=f"Chat with id: {request.chat_id} not found",
                error_type=ErrorType.NOT_FOUND,
            )

        public_chat.edit_description(
            description=request.new_description,
            current_date=self._time_provider.provide_current(),
            editor_id=current_user_id,
        )
