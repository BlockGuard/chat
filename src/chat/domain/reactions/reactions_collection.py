from chat.domain.reactions.exceptions import (
    ReactionAlreadySettedError,
    ReactionNotSettedError,
)
from chat.domain.reactions.reaction import Reaction
from chat.domain.reactions.reaction_id import ReactionId


class ReactionsCollection(set[Reaction]):
    def __init__(self) -> None:
        set.__init__(self)

    def add(self, element: Reaction) -> None:
        for reaction in self:
            if (
                reaction.entity_id == element.entity_id
                or reaction.user_id == element.user_id
            ):
                raise ReactionAlreadySettedError

        self.add(element)

    def get(self, reaction_id: ReactionId) -> Reaction:
        for reaction in self:
            if reaction.entity_id == reaction_id:
                return reaction

        raise ReactionNotSettedError
