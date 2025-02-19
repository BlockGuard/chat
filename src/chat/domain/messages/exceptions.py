from dataclasses import dataclass

from chat.domain.shared.exceptions import DomainError


@dataclass(frozen=True)
class UserNotOwnerOfMessageError(DomainError):
    message = "User not owner of message"
