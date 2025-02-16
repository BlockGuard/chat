from dataclasses import dataclass
from datetime import datetime

from chat.application.models.member import (
    ChatMember,
    PrivateChatMemberReadModel,
    PublicChatMemberReadModel,
)
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.chat_types import ChatType


@dataclass(frozen=True)
class ChatReadModel[MemberT: ChatMember]:
    chat_id: ChatId
    chat_type: ChatType
    created_at: datetime
    members: set[MemberT]


@dataclass(frozen=True)
class PrivateChatReadModel(ChatReadModel[PrivateChatMemberReadModel]):
    members: set[PrivateChatMemberReadModel]


@dataclass(frozen=True)
class PublicChatReadModel(ChatReadModel[PublicChatMemberReadModel]):
    title: str | None
    description: str | None
    members: set[PublicChatMemberReadModel]
