from chat.domain.shared.exceptions import DomainError


class OnlyReactionOwnerCanEditReactionError(DomainError):
    def __init__(self) -> None:
        DomainError.__init__(
            self,
            message="Only the reaction owner can edit the reaction",
        )


class ReactionNotSettedError(DomainError):
    def __init__(self) -> None:
        DomainError.__init__(self, message="Reaction not setted")


class ReactionAlreadySettedError(DomainError):
    def __init__(self) -> None:
        DomainError.__init__(self, message="Reaction already setted")
