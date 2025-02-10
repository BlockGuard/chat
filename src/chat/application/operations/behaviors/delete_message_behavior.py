from uuid import UUID

from bazario.asyncio import HandleNext, PipelineBehavior

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.operations.command.delete_message import DeleteMessage


class DeleteMessageBehavior(PipelineBehavior[DeleteMessage, None]):
    async def handle(
        self,
        request: DeleteMessage,
        handle_next: HandleNext[DeleteMessage, None],
    ) -> None:
        if not request.message_id:
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Message id is required",
            )

        if not isinstance(request.message_id, UUID):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Message id must be UUID",
            )

        await handle_next(request)
