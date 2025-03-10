from dataclasses import dataclass

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Command
from chat.application.ports.context import Context
from chat.application.ports.time_provider import TimeProvider
from chat.domain.messages.message_id import MessageId
from chat.domain.messages.repository import MessageRepository
from chat.domain.reactions.reaction_id import ReactionId


@dataclass(frozen=True)
class RemoveReaction(Command[None]):
    message_id: MessageId
    reaction_id: ReactionId


class RemoveReactionHandler(RequestHandler[RemoveReaction, None]):
    def __init__(
        self,
        context: Context,
        message_repository: MessageRepository,
        time_provider: TimeProvider,
    ) -> None:
        self._context = context
        self._message_repository = message_repository
        self._time_provider = time_provider

    async def handle(self, request: RemoveReaction) -> None:
        current_user_id = await self._context.user_id()

        message = await self._message_repository.with_message_id(
            message_id=request.message_id,
        )

        if not message:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Message {request.message_id} not found",
            )

        message.remove_reaction(
            reaction_id=request.reaction_id,
            user_id=current_user_id,
            current_date=self._time_provider.provide_current(),
        )
