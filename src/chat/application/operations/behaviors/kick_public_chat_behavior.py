from uuid import UUID

from bazario.asyncio import HandleNext, PipelineBehavior

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.operations.command.kick_public_chat_member import (
    KickPublicChatMember,
)


class KickPublicChatMemberBehavior(PipelineBehavior[KickPublicChatMember, None]):
    async def handle(
        self,
        request: KickPublicChatMember,
        handle_next: HandleNext[KickPublicChatMember, None],
    ) -> None:
        if not request.member_id:
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Member id is required",
            )

        if not request.chat_id:
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Chat id is required",
            )

        if not isinstance(request.member_id, UUID):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Member id must be UUID",
            )

        if not isinstance(request.chat_id, UUID):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Chat id must be UUID",
            )

        await handle_next(request)
