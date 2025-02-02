from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.command import Command
from chat.application.ports.time_provider import TimeProvider
from chat.domain.member.repository import MemberRepository
from chat.domain.message.events import MessageDeleted
from chat.domain.message.message_id import MessageId
from chat.domain.message.repository import MessageRepository
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class DeleteMessage(Command[None]):
    user_id: UserId
    message_id: MessageId


class DeleteMessageHandler(RequestHandler[DeleteMessage, None]):
    def __init__(
        self,
        time_provider: TimeProvider,
        message_repository: MessageRepository,
        member_repository: MemberRepository,
    ) -> None:
        self._time_provider = time_provider
        self._message_repository = message_repository
        self._member_repository = member_repository

    async def handle(self, request: DeleteMessage) -> None:
        message = await self._message_repository.with_message_id(
            message_id=request.message_id
        )

        if not message:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Message with id {request.message_id} not found",
            )

        message_owner = await self._member_repository.with_chat_id_and_user_id(
            user_id=message.owner_id,
            chat_id=message.chat_id,
        )

        if not message_owner:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="Member not found"
            )

        if message_owner.entity_id != request.user_id:
            raise ApplicationError(
                error_type=ErrorType.PERMISSION_ERROR,
                message="User is not message owner",
            )

        message.add_event(
            MessageDeleted(
                message_id=message.entity_id,
                owner_id=message.owner_id,
                chat_id=message.chat_id,
                event_date=self._time_provider.provide_current(),
            )
        )
        self._message_repository.delete(message)
