from dataclasses import dataclass
from datetime import datetime

from chat.domain.messages.message_id import MessageId
from chat.domain.reactions.reaction_id import ReactionId
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class ReactionReadModel:
    reaction_id: ReactionId
    message_id: MessageId
    user_id: UserId
    content: str
    set_at: datetime
