from dataclasses import dataclass

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Command
from chat.application.ports.context import Context
from chat.application.ports.time_provider import TimeProvider
from chat.domain.messages.events import MessageDeleted
from chat.domain.messages.message import Message
from chat.domain.messages.message_id import MessageId
from chat.domain.messages.repository import MessageRepository
from chat.domain.messages.specification import (
    MessageIdentifiedSpecification,
)
from chat.domain.shared.specification import Specification


@dataclass(frozen=True)
class DeleteMessage(Command):
    message_id: MessageId


class DeleteMessageHandler(RequestHandler[DeleteMessage, None]):
    def __init__(
        self,
        message_repository: MessageRepository,
        time_provider: TimeProvider,
        context: Context,
    ) -> None:
        self._message_repository = message_repository
        self._time_provider = time_provider
        self._context = context

    async def handle(self, request: DeleteMessage) -> None:
        specification = MessageIdentifiedSpecification(
            request.message_id
        )
        current_user_id = await self._context.user_id()

        message = await self._select(specification)

        if not message:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Message {request.message_id} not found",
            )

        if message.sender_id != current_user_id:
            raise ApplicationError(
                error_type=ErrorType.FORBIDDEN,
                message="You can't delete this message",
            )

        event = MessageDeleted(
            chat_id=message.chat_id,
            sender_id=message.sender_id,
            message_id=message.entity_id,
            event_date=self._time_provider.provide_current(),
        )
        message.remove_reactions()
        message.add_event(event)
        self._message_repository.delete(message)

    async def _select(
        self, specification: Specification[Message]
    ) -> Message | None:
        result = await self._message_repository.load(specification)
        return result.first()
