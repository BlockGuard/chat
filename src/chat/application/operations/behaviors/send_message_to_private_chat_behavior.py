from uuid import UUID

from bazario.asyncio import HandleNext, PipelineBehavior

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.operations.command.send_message_to_private_chat import (
    SendMessageToPrivateChat,
)
from chat.domain.message.message_id import MessageId


class SendMessageToPrivateChatBehavior(
    PipelineBehavior[SendMessageToPrivateChat, MessageId]
):
    async def handle(
        self,
        request: SendMessageToPrivateChat,
        handle_next: HandleNext[SendMessageToPrivateChat, MessageId],
    ) -> MessageId:
        if not request.chat_id:
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR, message="Chat ID is required"
            )

        if not request.content:
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR, message="Content is required"
            )

        if not isinstance(request.chat_id, UUID):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Chat ID must be a UUID",
            )

        if not isinstance(request.content, str):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Content must be a string",
            )

        response = await handle_next(request)

        return response
