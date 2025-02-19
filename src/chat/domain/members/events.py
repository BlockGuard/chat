from dataclasses import dataclass

from chat.domain.chats.chat_id import ChatId
from chat.domain.members.statuses import Status
from chat.domain.shared.events import DomainEvent
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class MemberJoinedChat(DomainEvent):
    chat_id: ChatId
    user_id: UserId


@dataclass(frozen=True)
class MemberStatusChanged(DomainEvent):
    chat_id: ChatId
    user_id: UserId
    status: Status


@dataclass(frozen=True)
class MemberLeftChat(DomainEvent):
    chat_id: ChatId
    user_id: UserId
