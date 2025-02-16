from dataclasses import dataclass, field

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Command
from chat.application.ports.context import Context
from chat.application.ports.id_generator import IdGenerator
from chat.application.ports.time_provider import TimeProvider
from chat.domain.message.message import Message
from chat.domain.message.message_id import MessageId
from chat.domain.message.repository import MessageRepository


@dataclass(frozen=True)
class DeleteMessage[MessageT: Message](Command[None]):
    message_id: MessageId
    content: str
    message_type: type[MessageT] = field(init=False)


class DeleteMessageHandler[MessageT: Message](
    RequestHandler[DeleteMessage[MessageT], None]
):
    def __init__(
        self,
        context: Context,
        message_repository: MessageRepository,
        id_generator: IdGenerator,
        time_provider: TimeProvider,
    ) -> None:
        self._context = context
        self._message_repository = message_repository
        self._id_generator = id_generator
        self._time_provider = time_provider

    async def handle(
        self,
        request: DeleteMessage[MessageT],
    ) -> None:
        current_user_id = await self._context.user_id()
        selected_message = self._message_repository.select(
            request.message_type
        )
        message = await selected_message.with_message_id(
            request.message_id
        )

        if not message:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message="Message not found",
            )

        if message.owner_id != current_user_id:
            raise ApplicationError(
                error_type=ErrorType.FORBIDDEN,
                message="You are not the owner of this message",
            )

        self._message_repository.delete(message)
