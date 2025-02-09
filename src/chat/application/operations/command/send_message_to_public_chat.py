from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.command import Command
from chat.application.ports.id_generator import IdGenerator
from chat.application.ports.identity_provider import IdentityProvider
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.repository import PublicChatRepository
from chat.domain.message.message_id import MessageId
from chat.domain.message.repository import MessageRepository


@dataclass(frozen=True)
class SendMessageToPublicChat(Command[MessageId]):
    chat_id: ChatId
    content: str


class SendMessageToPublicChatHandler(
    RequestHandler[SendMessageToPublicChat, MessageId]
):
    def __init__(
        self,
        public_chat_repository: PublicChatRepository,
        message_repository: MessageRepository,
        time_provider: TimeProvider,
        id_generator: IdGenerator,
        identity_provider: IdentityProvider,
    ) -> None:
        self._public_chat_repository = public_chat_repository
        self._message_repository = message_repository
        self._time_provider = time_provider
        self._id_generator = id_generator
        self._identity_provider = identity_provider

    async def handle(self, request: SendMessageToPublicChat) -> MessageId:
        current_user_id = await self._identity_provider.provide_current_user_id()
        public_chat = await self._public_chat_repository.with_chat_id(
            chat_id=request.chat_id
        )

        if not public_chat:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Chat with id {request.chat_id} not found",
            )

        message = public_chat.send_message_to_public_chat(
            sender_id=current_user_id,
            message_id=self._id_generator.generate_message_id(),
            content=request.content,
            current_date=self._time_provider.provide_current(),
        )

        self._message_repository.add(message=message)

        return message.entity_id
