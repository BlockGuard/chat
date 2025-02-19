from dataclasses import dataclass

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Command
from chat.application.ports.context import Context
from chat.application.ports.time_provider import TimeProvider
from chat.domain.messages.message import Message
from chat.domain.messages.message_id import MessageId
from chat.domain.messages.repository import MessageRepository
from chat.domain.messages.specification import (
    MessageIdentifiedSpecification,
)
from chat.domain.reactions.reaction_id import ReactionId
from chat.domain.shared.specification import Specification


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
        specification = MessageIdentifiedSpecification(
            request.message_id
        )
        current_user_id = await self._context.user_id()

        message = await self._select(specification)

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

    async def _select(
        self, specification: Specification[Message]
    ) -> Message | None:
        result = await self._message_repository.load(specification)
        return result.first()
