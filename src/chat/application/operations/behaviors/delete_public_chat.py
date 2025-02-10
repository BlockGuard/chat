from uuid import UUID

from bazario.asyncio import HandleNext, PipelineBehavior

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.operations.command.delete_public_chat import DeletePublicChat


class DeletePublicChatBehavior(PipelineBehavior[DeletePublicChat, None]):
    async def handle(
        self,
        request: DeletePublicChat,
        handle_next: HandleNext[DeletePublicChat, None],
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

        await handle_next(request)
