from uuid import UUID

from bazario.asyncio import HandleNext, PipelineBehavior

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.operations.command.change_private_chat_member_status import (
    ChangePrivateChatMemberStatus,
)
from chat.domain.member.statuses import MemberStatus


class ChangePrivateChatMemberStatusBehavior(
    PipelineBehavior[ChangePrivateChatMemberStatus, None]
):
    async def handle(
        self,
        request: ChangePrivateChatMemberStatus,
        handle_next: HandleNext[ChangePrivateChatMemberStatus, None],
    ) -> None:
        if not request.chat_id:
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR, message="Chat id is required"
            )

        if not request.member_id:
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="Member id is required",
            )

        if not request.new_status:
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message="New status is required",
            )

        if not isinstance(request.chat_id, UUID):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message=f"Chat id must be UUID, not {type(request.chat_id)}",
            )

        if not isinstance(request.member_id, UUID):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message=f"Member id must be UUID, not {type(request.member_id)}",
            )

        if request.new_status not in list(MemberStatus):
            raise ApplicationError(
                error_type=ErrorType.VALIDATION_ERROR,
                message=f"New status must be one of {list(MemberStatus)}",
            )

        await handle_next(request)
