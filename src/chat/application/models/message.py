from dataclasses import dataclass
from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.message.message_id import MessageId
from chat.domain.shared.user_id import UserId


@dataclass(frozen=True)
class MessageReadModel:
    chat_id: ChatId
    message_id: MessageId
    sender_id: UserId
    content: str
    sended_at: datetime
    updated_at: datetime | None
