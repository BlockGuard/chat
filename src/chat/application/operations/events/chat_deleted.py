from bazario.asyncio import NotificationHandler

from chat.domain.chat.events import PublicChatDeleted
from chat.domain.message.repository import MessageRepository


class ChatDeletedHandler(NotificationHandler[PublicChatDeleted]):
    def __init__(self, message_repository: MessageRepository) -> None:
        self._message_repository = message_repository

    async def handle(self, notification: PublicChatDeleted) -> None:
        chat_messages = await self._message_repository.with_chat_id(
            chat_id=notification.chat_id
        )
        self._message_repository.delete_many(chat_messages)
