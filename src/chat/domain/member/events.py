from dataclasses import dataclass

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.member_id import MemberId
from chat.domain.shared.events import DomainEvent


@dataclass(frozen=True)
class MemberJoined(DomainEvent):
    member_id: MemberId
    chat_id: ChatId


@dataclass(frozen=True)
class MemberLeft(DomainEvent):
    member_id: MemberId
    chat_id: ChatId
