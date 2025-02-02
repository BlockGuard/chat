from dataclasses import dataclass

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.roles import MemberRole
from chat.domain.shared.events import DomainEvent
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class MemberJoined(DomainEvent):
    member_id: UserId
    chat_id: ChatId
    role: MemberRole


@dataclass(frozen=True)
class MemberLeft(DomainEvent):
    member_id: UserId
    chat_id: ChatId


@dataclass(frozen=True)
class MemberRoleChanged(DomainEvent):
    member_id: UserId
    chat_id: ChatId
    role: MemberRole
