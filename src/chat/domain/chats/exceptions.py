from dataclasses import dataclass

from chat.domain.shared.exceptions import DomainError


@dataclass(frozen=True)
class LimitOfMembersReachedError(DomainError):
    message: str = "Limit of members reached"
