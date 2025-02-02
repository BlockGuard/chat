from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.command import Command
from chat.application.ports.time_provider import TimeProvider
from chat.domain.invitation.invitation_id import InvitationId
from chat.domain.invitation.repository import InvitationRepository
from chat.domain.invitation.statuses import InvitationStatus
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class RejectChatInvitation(Command[None]):
    user_id: UserId
    invitation_id: InvitationId


class RejectChatInvitationHandler(RequestHandler[RejectChatInvitation, None]):
    def __init__(
        self,
        time_provider: TimeProvider,
        invitation_repository: InvitationRepository,
    ) -> None:
        self._time_provider = time_provider
        self._invitation_repository = invitation_repository

    async def handle(self, request: RejectChatInvitation) -> None:
        invitation = await self._invitation_repository.with_invitation_id(
            invitation_id=request.invitation_id
        )

        if not invitation:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="Invitation not found"
            )

        if invitation.expires_at < self._time_provider.provide_current():
            raise ApplicationError(
                error_type=ErrorType.BAD_REQUEST, message="Invitation expired"
            )

        if invitation.status != InvitationStatus.PENDING:
            raise ApplicationError(
                error_type=ErrorType.BAD_REQUEST,
                message="Invitation is not pending",
            )

        invitation.change_status(
            status=InvitationStatus.REJECTED,
            current_date=self._time_provider.provide_current(),
        )
