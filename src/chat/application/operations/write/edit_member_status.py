from dataclasses import dataclass, field

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Command
from chat.application.ports.context import Context
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.base_chat import BaseChat
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.repository import ChatRepository
from chat.domain.member.statuses import MemberStatus
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class EditMemberStatus[ChatT: BaseChat](Command[None]):
    chat_id: ChatId
    member_id: UserId
    status: MemberStatus
    chat_type: type[ChatT] = field(init=False)


class EditMemberStatusHandler[ChatT: BaseChat](
    RequestHandler[EditMemberStatus, None]
):
    def __init__(
        self,
        repository: ChatRepository,
        context: Context,
        time_provider: TimeProvider,
    ) -> None:
        self._repository = repository
        self._context = context
        self._time_provider = time_provider

    async def handle(self, request: EditMemberStatus[ChatT]) -> None:
        current_user_id = await self._context.user_id()
        selected_chat = self._repository.select(request.chat_type)
        chat = await selected_chat.with_chat_id(request.chat_id)

        if not chat:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message="Chat not found",
            )

        chat.edit_member_status(
            member_id=request.member_id,
            status=request.status,
            editor_id=current_user_id,
            current_date=self._time_provider.provide_current(),
        )
