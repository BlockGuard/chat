from dataclasses import dataclass
from datetime import datetime

from chat.application.models.reaction import ReactionReadModel
from chat.domain.chats.chat_id import ChatId
from chat.domain.messages.message_id import MessageId
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class MessageReadModel:
    message_id: MessageId
    chat_id: ChatId
    user_id: UserId
    content: str
    sent_at: datetime
    edited_at: datetime | None
    reactions: set[ReactionReadModel]
