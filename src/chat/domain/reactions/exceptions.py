from dataclasses import dataclass

from chat.domain.shared.exceptions import DomainError


@dataclass(frozen=True)
class OnlyReactionOwnerCanEditReactionError(DomainError):
    message = "Only the reaction owner can edit the reaction"


@dataclass(frozen=True)
class ReactionNotSettedError(DomainError):
    message = "Reaction not setted"


@dataclass(frozen=True)
class ReactionAlreadySettedError(DomainError):
    message = "Reaction already setted"
