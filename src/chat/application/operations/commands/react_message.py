from dataclasses import dataclass

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Command
from chat.application.ports.context import Context
from chat.application.ports.id_generator import IdGenerator
from chat.application.ports.time_provider import TimeProvider
from chat.domain.messages.message_id import MessageId
from chat.domain.messages.repository import MessageRepository
from chat.domain.reactions.reaction_id import ReactionId


@dataclass(frozen=True)
class ReactMessage(Command[ReactionId]):
    message_id: MessageId
    reaction: str


class ReactMessageHandler(RequestHandler[ReactMessage, ReactionId]):
    def __init__(
        self,
        message_repository: MessageRepository,
        id_generator: IdGenerator,
        time_provider: TimeProvider,
        context: Context,
    ) -> None:
        self._message_repository = message_repository
        self._id_generator = id_generator
        self._time_provider = time_provider
        self._context = context

    async def handle(self, request: ReactMessage) -> ReactionId:
        current_user_id = await self._context.user_id()

        message = await self._message_repository.with_message_id(
            message_id=request.message_id
        )

        if not message:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Message {request.message_id} not found",
            )

        reaction = message.add_reaction(
            reaction_id=self._id_generator.generate_reaction_id(),
            content=request.reaction,
            user_id=current_user_id,
            current_date=self._time_provider.provide_current(),
        )

        return reaction.entity_id
