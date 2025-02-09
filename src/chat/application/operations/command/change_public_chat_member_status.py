from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.command import Command
from chat.application.ports.identity_provider import IdentityProvider
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.repository import PublicChatRepository
from chat.domain.member.statuses import MemberStatus
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class ChangePublicChatMemberStatus(Command[None]):
    chat_id: ChatId
    member_id: UserId
    new_status: MemberStatus


class ChangePublicChatMemberStatusHandler(
    RequestHandler[ChangePublicChatMemberStatus, None]
):
    def __init__(
        self,
        time_provider: TimeProvider,
        private_chat_repository: PublicChatRepository,
        identity_provider: IdentityProvider,
    ) -> None:
        self._time_provider = time_provider
        self._private_chat_repository = private_chat_repository
        self._identity_provider = identity_provider

    async def handle(self, request: ChangePublicChatMemberStatus) -> None:
        current_user_id = await self._identity_provider.provide_current_user_id()
        public_chat = await self._private_chat_repository.with_chat_id(
            chat_id=request.chat_id
        )

        if not public_chat:
            raise ApplicationError(
                message=f"Chat with id: {request.chat_id} not found",
                error_type=ErrorType.NOT_FOUND,
            )

        public_chat.change_member_status(
            member_id=request.member_id,
            status=request.new_status,
            changed_by_id=current_user_id,
            current_date=self._time_provider.provide_current(),
        )
