from dataclasses import dataclass
from datetime import datetime

from chat.application.models.member import MemberReadModel
from chat.domain.chat.chat_id import ChatId
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class ChatReadModel:
    chat_id: ChatId
    created_at: datetime
    members: set[MemberReadModel]
    updated_at: datetime
    description: str | None
    title: str | None

    def ensure_is_member(self, user_id: UserId) -> bool:
        return any(member.member_id == user_id for member in self.members)
