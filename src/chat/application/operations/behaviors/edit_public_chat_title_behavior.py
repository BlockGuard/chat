from uuid import UUID

from bazario.asyncio import HandleNext, PipelineBehavior

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.operations.command.edit_public_chat_title import (
    EditPublicChatTitle,
)


class EditPublicChatTitleBehavior(PipelineBehavior[EditPublicChatTitle, None]):
    async def handle(
        self,
        request: EditPublicChatTitle,
        handle_next: HandleNext[EditPublicChatTitle, None],
    ) -> None:
        if not request.chat_id:
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Chat id is required",
            )

        if not isinstance(request.chat_id, UUID):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Chat id must be UUID",
            )

        if request.new_title and not isinstance(request.new_title, str):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="New title must be string",
            )

        await handle_next(request)
