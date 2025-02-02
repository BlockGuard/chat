from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.common.markers.command import Command
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.chat_types import ChatType
from chat.domain.chat.repository import ChatRepository
from chat.domain.member.repository import MemberRepository
from chat.domain.member.roles import MemberRole
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class EditPublicChat(Command[None]):
    user_id: UserId
    chat_id: ChatId
    title: str
    description: str


class EditPublicChatHandler(RequestHandler[EditPublicChat, None]):
    def __init__(
        self,
        chat_repository: ChatRepository,
        time_provider: TimeProvider,
        member_repository: MemberRepository,
    ) -> None:
        self._chat_repository = chat_repository
        self._time_provider = time_provider
        self._member_repository = member_repository

    async def handle(self, request: EditPublicChat) -> None:
        chat_member = await self._member_repository.with_chat_id_and_user_id(
            user_id=request.user_id, chat_id=request.chat_id
        )

        if not chat_member:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message="You are not a part of this chat",
            )

        chat = await self._chat_repository.with_chat_id(chat_id=request.chat_id)

        if not chat:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="Chat not found"
            )

        if chat.chat_type != ChatType.PUBLIC:
            raise ApplicationError(
                error_type=ErrorType.PERMISSION_ERROR,
                message="You are not allowed to edit this chat",
            )

        if chat.owner_id != request.user_id or chat_member.role != MemberRole.ADMIN:
            raise ApplicationError(
                error_type=ErrorType.PERMISSION_ERROR,
                message="You are not allowed to edit this chat",
            )

        chat.edit_chat(
            title=request.title,
            description=request.description,
            current_time=self._time_provider.provide_current(),
        )
