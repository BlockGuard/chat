from dataclasses import dataclass
from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.roles import MemberRole
from chat.domain.member.statuses import MemberStatus
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class ChatMember:
    chat_id: ChatId
    user_id: UserId
    status: MemberStatus
    joined_at: datetime


@dataclass(frozen=True)
class PrivateChatMemberReadModel(ChatMember): ...


@dataclass(frozen=True)
class PublicChatMemberReadModel(ChatMember):
    role: MemberRole
