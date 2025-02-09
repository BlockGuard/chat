from dataclasses import dataclass
from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.roles import MemberRole
from chat.domain.member.statuses import MemberStatus
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class MemberReadModel:
    member_id: UserId
    chat_id: ChatId
    joined_at: datetime
    status: MemberStatus
    role: MemberRole
