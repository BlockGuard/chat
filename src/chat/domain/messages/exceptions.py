from chat.domain.shared.exceptions import DomainError


class UserNotOwnerOfMessageError(DomainError):
    def __init__(self) -> None:
        DomainError.__init__(
            self, message="User not owner of message"
        )
