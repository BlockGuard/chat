from datetime import datetime

from chat.domain.messages.message_id import MessageId
from chat.domain.reactions.exceptions import (
    OnlyReactionOwnerCanOperateWithReactionError,
)
from chat.domain.reactions.reaction_id import ReactionId
from chat.domain.shared.entity import Entity
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class Reaction(Entity[ReactionId]):
    def __init__(
        self,
        entity_id: ReactionId,
        unit_of_work: UnitOfWork,
        event_adder: DomainEventAdder,
        *,
        message_id: MessageId,
        user_id: UserId,
        reaction: str,
        set_at: datetime,
    ) -> None:
        Entity.__init__(self, entity_id, event_adder, unit_of_work)

        self._message_id = message_id
        self._user_id = user_id
        self._reaction = reaction
        self._set_at = set_at

    def ensure_owner(self, user_id: UserId) -> None:
        if user_id != self._user_id:
            raise OnlyReactionOwnerCanOperateWithReactionError

    @property
    def message_id(self) -> MessageId:
        return self._message_id

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def reaction(self) -> str:
        return self._reaction

    @property
    def set_at(self) -> datetime:
        return self._set_at
