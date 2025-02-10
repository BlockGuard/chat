from uuid import UUID

from bazario.asyncio import HandleNext, PipelineBehavior

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.operations.command.edit_public_chat_description import (
    EditPublicChatDescription,
)


class EditPublicChatDescriptionBehavior(
    PipelineBehavior[EditPublicChatDescription, None]
):
    async def handle(
        self,
        request: EditPublicChatDescription,
        handle_next: HandleNext[EditPublicChatDescription, None],
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

        if request.new_description and not isinstance(request.new_description, str):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="New description must be string",
            )

        await handle_next(request)
