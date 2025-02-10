from uuid import UUID

from bazario.asyncio import HandleNext, PipelineBehavior

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.operations.command.create_private_chat import CreatePrivateChat
from chat.domain.chat.chat_id import ChatId


class CreatePrivateChatBehavior(PipelineBehavior[CreatePrivateChat, ChatId]):
    async def handle(
        self,
        request: CreatePrivateChat,
        handle_next: HandleNext[CreatePrivateChat, ChatId],
    ) -> ChatId:
        if not request.companion_id:
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Companion id is required",
            )

        if not isinstance(request.companion_id, UUID):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Companion id must be UUID",
            )

        response = await handle_next(request)

        return response
