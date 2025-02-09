from dataclasses import dataclass
from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.message.message_id import MessageId
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class MessageReadModel:
    message_id: MessageId
    chat_id: ChatId
    sender_id: UserId
    content: str
    sended_at: datetime
    edited_at: datetime | None
