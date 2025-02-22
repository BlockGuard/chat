from dataclasses import dataclass
from datetime import datetime

from chat.domain.chats.chat_id import ChatId
from chat.domain.members.statuses import Status
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class ChatMemberReadModel:
    chat_id: ChatId
    user_id: UserId
    status: Status
    joined_at: datetime
