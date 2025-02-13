from dataclasses import dataclass

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.member import Member
from chat.domain.member.private_chat_member import PrivateChatMember
from chat.domain.member.public_chat_member import PublicChatMember
from chat.domain.member.roles import MemberRole
from chat.domain.member.statuses import MemberStatus
from chat.domain.shared.events import DomainEvent
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class MemberJoinedChat[MemberT: Member](DomainEvent[MemberT]):
    chat_id: ChatId
    user_id: UserId
    status: MemberStatus


@dataclass(frozen=True)
class MemberJoinedPrivateChat(
    MemberJoinedChat[PrivateChatMember]
): ...


@dataclass(frozen=True)
class MemberJoinedPublicChat(MemberJoinedChat[PublicChatMember]):
    role: MemberRole


@dataclass(frozen=True)
class MemberRoleChanged(DomainEvent[PublicChatMember]):
    chat_id: ChatId
    user_id: UserId
    role: MemberRole


@dataclass(frozen=True)
class MemberStatusChanged[MemberT: Member](DomainEvent[MemberT]):
    chat_id: ChatId
    user_id: UserId
    status: MemberStatus


@dataclass(frozen=True)
class PrivateChatMemberStatusChanged(
    MemberStatusChanged[PrivateChatMember]
): ...


@dataclass(frozen=True)
class PublicChatMemberStatusChanged(
    MemberStatusChanged[PublicChatMember]
): ...


@dataclass(frozen=True)
class MemberLeftChat[MemberT: Member](DomainEvent[Member]):
    chat_id: ChatId
    user_id: UserId


@dataclass(frozen=True)
class PrivateChatMemberLeftChat(
    MemberLeftChat[PrivateChatMember]
): ...


@dataclass(frozen=True)
class PublicChatMemberLeftChat(MemberLeftChat[PublicChatMember]): ...
