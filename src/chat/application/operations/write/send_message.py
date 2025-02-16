from dataclasses import dataclass, field

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.handlers import RequestHandler
from chat.application.common.markers import Command
from chat.application.ports.context import Context
from chat.application.ports.id_generator import IdGenerator
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.base_chat import BaseChat
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.repository import ChatRepository
from chat.domain.message.message_id import MessageId
from chat.domain.message.repository import MessageRepository


@dataclass(frozen=True)
class SendMessage[ChatT: BaseChat](Command[MessageId]):
    chat_id: ChatId
    content: str
    chat_type: type[ChatT] = field(init=False)


class SendMessageHandler[ChatT: BaseChat](
    RequestHandler[SendMessage[ChatT], MessageId]
):
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

    async def handle(self, request: SendMessage[ChatT]) -> MessageId:
        current_user_id = await self._context.user_id()
        selected_chat = self._chat_repository.select(
            request.chat_type
        )
        chat = await selected_chat.with_chat_id(request.chat_id)

        if not chat:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message="Chat not found",
            )

        message = chat.send_message(
            sender_id=current_user_id,
            message_id=self._id_generator.generate_message_id(),
            content=request.content,
            current_date=self._time_provider.provide_current(),
        )

        self._message_repository.add(message)

        return message.entity_id
