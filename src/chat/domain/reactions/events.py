from dataclasses import dataclass

from chat.domain.messages.message_id import MessageId
from chat.domain.reactions.reaction_id import ReactionId
from chat.domain.shared.events import DomainEvent
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class ReactionAdded(DomainEvent):
    message_id: MessageId
    user_id: UserId
    reaction_id: ReactionId
    reaction: str


@dataclass(frozen=True)
class ReactionRemoved(DomainEvent):
    message_id: MessageId
    user_id: UserId
    reaction_id: ReactionId
