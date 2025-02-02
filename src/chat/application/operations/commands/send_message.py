from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.command import Command
from chat.application.ports.id_generator import IdGenerator
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.member.repository import MemberRepository
from chat.domain.message.message_id import MessageId
from chat.domain.message.repository import MessageRepository
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class SendMessage(Command[MessageId]):
    user_id: UserId
    chat_id: ChatId
    content: str


class SendMessageHandler(RequestHandler[SendMessage, MessageId]):
    def __init__(
        self,
        message_repository: MessageRepository,
        member_repository: MemberRepository,
        time_provider: TimeProvider,
        id_generator: IdGenerator,
    ) -> None:
        self._message_repository = message_repository
        self._member_repository = member_repository
        self._time_provider = time_provider
        self._id_generator = id_generator

    async def handle(self, request: SendMessage) -> MessageId:
        member = await self._member_repository.with_chat_id_and_user_id(
            user_id=request.user_id, chat_id=request.chat_id
        )

        if not member:
            raise ApplicationError(
                message="You are not a part of this chat",
                error_type=ErrorType.NOT_FOUND,
            )

        message = member.send_message(
            message_id=self._id_generator.generate_message_id(),
            content=request.content,
            current_date=self._time_provider.provide_current(),
        )
        self._message_repository.add(message)

        return message.entity_id
