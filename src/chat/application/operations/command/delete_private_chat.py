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
from chat.domain.chat.repository import PrivateChatRepository


@dataclass(frozen=True)
class DeletePrivateChat(Command[None]):
    chat_id: ChatId


class DeletePrivateChatHandler(RequestHandler[DeletePrivateChat, None]):
    def __init__(
        self,
        time_provider: TimeProvider,
        private_chat_repository: PrivateChatRepository,
        identity_provider: IdentityProvider,
    ) -> None:
        self._time_provider = time_provider
        self._private_chat_repository = private_chat_repository
        self._identity_provider = identity_provider

    async def handle(self, request: DeletePrivateChat) -> None:
        current_user_id = await self._identity_provider.provide_current_user_id()
        private_chat = await self._private_chat_repository.with_chat_id(
            chat_id=request.chat_id
        )

        if not private_chat:
            raise ApplicationError(
                message=f"Chat with id: {request.chat_id} not found",
                error_type=ErrorType.NOT_FOUND,
            )

        private_chat.delete_private_chat(
            deleter_id=current_user_id,
            current_date=self._time_provider.provide_current(),
        )
