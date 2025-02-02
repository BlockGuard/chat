from bazario.asyncio import NotificationHandler

from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.events import ChatDeleted
from chat.domain.member.repository import MemberRepository
from chat.domain.message.repository import MessageRepository


class ChatDeletedHandler(NotificationHandler[ChatDeleted]):
    def __init__(
        self,
        member_repository: MemberRepository,
        message_repository: MessageRepository,
    ) -> None:
        self._member_repository = member_repository
        self._message_repository = message_repository

    async def handle(self, notification: ChatDeleted) -> None:
        await self._delete_chat_members(notification.chat_id)
        await self._delete_chat_messages(notification.chat_id)

    async def _delete_chat_messages(self, chat_id: ChatId) -> None:
        chat_messages = await self._message_repository.with_chat_id(chat_id=chat_id)

        self._message_repository.delete_many(chat_messages)

    async def _delete_chat_members(self, chat_id: ChatId) -> None:
        chat_members = await self._member_repository.with_chat_id(chat_id=chat_id)

        self._member_repository.delete_many(chat_members)
