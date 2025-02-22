from dataclasses import dataclass

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Command
from chat.application.ports.context import Context
from chat.application.ports.time_provider import TimeProvider
from chat.domain.messages.message_id import MessageId
from chat.domain.messages.repository import MessageRepository


@dataclass(frozen=True)
class EditMessage(Command):
    message_id: MessageId
    text: str


class EditMessageHandler(RequestHandler[EditMessage, None]):
    def __init__(
        self,
        context: Context,
        message_repository: MessageRepository,
        time_provider: TimeProvider,
    ) -> None:
        self._context = context
        self._message_repository = message_repository
        self._time_provider = time_provider

    async def handle(self, request: EditMessage) -> None:
        current_user_id = await self._context.user_id()
        message = await self._message_repository.with_message_id(
            message_id=request.message_id
        )

        if not message:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message="Message not found",
            )

        if message.sender_id != current_user_id:
            raise ApplicationError(
                error_type=ErrorType.FORBIDDEN,
                message="You can't edit this message",
            )

        message.edit_message(
            new_text=request.text,
            current_date=self._time_provider.provide_current(),
        )
