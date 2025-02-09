from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.command import Command
from chat.application.ports.identity_provider import IdentityProvider
from chat.application.ports.time_provider import TimeProvider
from chat.domain.message.events import MessageDeleted
from chat.domain.message.message_id import MessageId
from chat.domain.message.repository import MessageRepository


@dataclass(frozen=True)
class DeleteMessage(Command[None]):
    message_id: MessageId


class DeleteMessageHandler(RequestHandler[DeleteMessage, None]):
    def __init__(
        self,
        time_provider: TimeProvider,
        message_repository: MessageRepository,
        identity_provider: IdentityProvider,
    ) -> None:
        self._time_provider = time_provider
        self._message_repository = message_repository
        self._identity_provider = identity_provider

    async def handle(self, request: DeleteMessage) -> None:
        current_user_id = await self._identity_provider.provide_current_user_id()
        message = await self._message_repository.with_message_id(
            message_id=request.message_id
        )

        if not message:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Message with id: {request.message_id} not found",
            )

        if message.owner_id != current_user_id:
            raise ApplicationError(
                error_type=ErrorType.FORBIDDEN,
                message="You are not allowed to delete this message",
            )

        message.add_event(
            MessageDeleted(
                chat_id=message.chat_id,
                message_id=message.entity_id,
                sender_id=message.owner_id,
                event_date=self._time_provider.provide_current(),
            )
        )

        self._message_repository.delete(message=message)
