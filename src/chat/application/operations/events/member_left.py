from chat.application.common.handlers import NotificationHandler
from chat.domain.member.events import MemberLeftChat
from chat.domain.message.repository import MessageRepository


class MemberLeftChatHandler[EventT: MemberLeftChat](
    NotificationHandler[EventT]
):
    def __init__(self, message_repository: MessageRepository) -> None:
        self._message_repository = message_repository

    async def handle(self, notification: EventT) -> None:
        selected_message = self._message_repository.select(
            notification.entity_type
        )
        messages = await selected_message.with_chat_id(
            notification.chat_id
        )

        self._message_repository.delete_many(messages)
