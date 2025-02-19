from dataclasses import dataclass

from chat.domain.shared.exceptions import DomainError


@dataclass(frozen=True)
class MemberNotInChatError(DomainError):
    message = "Member not in chat"


@dataclass(frozen=True)
class MemberAlreadyInChatError(DomainError):
    message = "Member already in chat"


@dataclass(frozen=True)
class BlockedMemberCantSendMessageError(DomainError):
    message = "Blocked member can't send message"
