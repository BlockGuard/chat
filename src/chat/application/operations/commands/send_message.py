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
from chat.domain.chats.chat_id import ChatId
from chat.domain.chats.chat_room import ChatRoom
from chat.domain.chats.repository import ChatRepository
from chat.domain.chats.specification import (
    ChatIdentifiedSpecification,
)
from chat.domain.messages.message_id import MessageId
from chat.domain.messages.repository import MessageRepository
from chat.domain.shared.specification import Specification


@dataclass(frozen=True)
class SendMessage(Command[MessageId]):
    chat_id: ChatId
    text: str


class SendMessageHandler(RequestHandler[SendMessage, MessageId]):
    def __init__(
        self,
        chat_repository: ChatRepository,
        message_repository: MessageRepository,
        id_generator: IdGenerator,
        time_provider: TimeProvider,
        context: Context,
    ) -> None:
        self._chat_repository = chat_repository
        self._message_repository = message_repository
        self._id_generator = id_generator
        self._time_provider = time_provider
        self._context = context

    async def handle(self, request: SendMessage) -> MessageId:
        specification = ChatIdentifiedSpecification(request.chat_id)
        current_user_id = await self._context.user_id()

        chat = await self._select(specification)

        if not chat:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Chat with id {request.chat_id} not found",
            )

        message = chat.send_message(
            sender_id=current_user_id,
            content=request.text,
            message_id=self._id_generator.generate_message_id(),
            current_date=self._time_provider.provide_current(),
        )

        self._message_repository.add(message)

        return message.entity_id

    async def _select(
        self, specification: Specification[ChatRoom]
    ) -> ChatRoom | None:
        result = await self._chat_repository.load(specification)
        return result.first()
