from uuid import UUID

from bazario.asyncio import HandleNext, PipelineBehavior

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.operations.command.edit_message_content import (
    EditMessageContent,
)


class EditMessageContentBehavior(PipelineBehavior[EditMessageContent, None]):
    async def handle(
        self,
        request: EditMessageContent,
        handle_next: HandleNext[EditMessageContent, None],
    ) -> None:
        if not request.message_id:
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Message id is required",
            )

        if not request.content:
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Content is required",
            )

        if not isinstance(request.message_id, UUID):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Message id must be UUID",
            )

        if not isinstance(request.content, str):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Content must be string",
            )

        await handle_next(request)
