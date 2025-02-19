from datetime import datetime

from chat.domain.chats.chat_id import ChatId
from chat.domain.messages.events import MessageEdited
from chat.domain.messages.message_id import MessageId
from chat.domain.reactions.events import (
    ReactionAdded,
    ReactionRemoved,
)
from chat.domain.reactions.reaction import Reaction
from chat.domain.reactions.reaction_id import ReactionId
from chat.domain.reactions.reactions_collection import (
    ReactionsCollection,
)
from chat.domain.shared.entity import Entity
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class Message(Entity[MessageId]):
    def __init__(
        self,
        entity_id: MessageId,
        unit_of_work: UnitOfWork,
        event_adder: DomainEventAdder,
        *,
        sender_id: UserId,
        chat_id: ChatId,
        text: str,
        sent_at: datetime,
        edited_at: datetime | None,
        reactions: ReactionsCollection,
    ) -> None:
        Entity.__init__(self, entity_id, event_adder, unit_of_work)

        self._sender_id = sender_id
        self._chat_id = chat_id
        self._text = text
        self._sent_at = sent_at
        self._edited_at = edited_at
        self._reactions = reactions

    def add_reaction(
        self,
        reaction_id: ReactionId,
        content: str,
        user_id: UserId,
        current_date: datetime,
    ) -> Reaction:
        reaction = Reaction(
            entity_id=reaction_id,
            unit_of_work=self._unit_of_work,
            event_adder=self._event_adder,
            user_id=user_id,
            reaction=content,
            message_id=self._entity_id,
            set_at=current_date,
        )
        event = ReactionAdded(
            message_id=self._entity_id,
            user_id=user_id,
            reaction_id=reaction_id,
            reaction=content,
            event_date=current_date,
        )
        self._reactions.add(reaction)
        reaction.mark_new()
        reaction.add_event(event)
        return reaction

    def remove_reaction(
        self,
        reaction_id: ReactionId,
        user_id: UserId,
        current_date: datetime,
    ) -> None:
        reaction = self._reactions.get(reaction_id)
        reaction.ensure_owner(user_id)
        self._reactions.remove(reaction)
        event = ReactionRemoved(
            message_id=self._entity_id,
            user_id=user_id,
            reaction_id=reaction_id,
            event_date=current_date,
        )
        reaction.add_event(event)
        reaction.mark_deleted()

    def edit_message(
        self, new_text: str, current_date: datetime
    ) -> None:
        self._text = new_text
        self._edited_at = current_date
        event = MessageEdited(
            message_id=self._entity_id,
            sender_id=self._sender_id,
            new_content=new_text,
            chat_id=self._chat_id,
            event_date=current_date,
        )
        self.add_event(event)
        self.mark_dirty()

    def remove_reactions(self) -> None:
        self._reactions.clear()

    @property
    def sender_id(self) -> UserId:
        return self._sender_id

    @property
    def chat_id(self) -> ChatId:
        return self._chat_id

    @property
    def text(self) -> str:
        return self._text

    @property
    def sent_at(self) -> datetime:
        return self._sent_at

    @property
    def edited_at(self) -> datetime | None:
        return self._edited_at

    @property
    def reactions(self) -> set[Reaction]:
        return self._reactions
