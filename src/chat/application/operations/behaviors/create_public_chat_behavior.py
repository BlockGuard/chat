from bazario.asyncio import HandleNext, PipelineBehavior

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.operations.command.create_public_chat import CreatePublicChat
from chat.domain.chat.chat_id import ChatId


class CreatePublicChatBehavior(PipelineBehavior[CreatePublicChat, ChatId]):
    async def handle(
        self,
        request: CreatePublicChat,
        handle_next: HandleNext[CreatePublicChat, ChatId],
    ) -> ChatId:
        if request.description and not isinstance(request.description, str):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Description must be string",
            )

        if request.title and not isinstance(request.title, str):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Title must be string",
            )

        response = await handle_next(request)

        return response
