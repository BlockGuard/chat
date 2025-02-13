from dataclasses import dataclass

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.roles import MemberRole
from chat.domain.member.statuses import MemberStatus
from chat.domain.shared.events import DomainEvent
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class MemberJoinedChat(DomainEvent):
    chat_id: ChatId
    user_id: UserId
    status: MemberStatus


@dataclass(frozen=True)
class MemberJoinedPrivateChat(MemberJoinedChat): ...


@dataclass(frozen=True)
class MemberJoinedPublicChat(MemberJoinedChat):
    role: MemberRole


@dataclass(frozen=True)
class MemberRoleChanged(DomainEvent):
    chat_id: ChatId
    user_id: UserId
    role: MemberRole


@dataclass(frozen=True)
class MemberStatusChanged(DomainEvent):
    chat_id: ChatId
    user_id: UserId
    status: MemberStatus


@dataclass(frozen=True)
class PrivateChatMemberStatusChanged(MemberStatusChanged): ...


@dataclass(frozen=True)
class PublicChatMemberStatusChanged(MemberStatusChanged): ...


@dataclass(frozen=True)
class MemberLeftChat(DomainEvent):
    chat_id: ChatId
    user_id: UserId


@dataclass(frozen=True)
class PrivateChatMemberLeftChat(MemberLeftChat): ...


@dataclass(frozen=True)
class PublicChatMemberLeftChat(MemberLeftChat): ...
