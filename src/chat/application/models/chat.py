from dataclasses import dataclass
from datetime import datetime

from chat.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from chat.application.models.member import ChatMemberReadModel
from chat.domain.chats.chat_id import ChatId
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class ChatReadModel:
    chat_id: ChatId
    created_at: datetime
    members: set[ChatMemberReadModel]

    def ensure_member(self, member_id: UserId) -> None:
        if not any(member.user_id == member_id for member in self.members):
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message="You are not a member of this chat",
            )
