from bazario.asyncio import NotificationHandler

from chat.domain.member.events import MemberLeft
from chat.domain.message.repository import MessageRepository


class MemberLeftHandler(NotificationHandler[MemberLeft]):
    def __init__(
        self,
        message_repository: MessageRepository,
    ) -> None:
        self._message_repository = message_repository

    async def handle(self, notification: MemberLeft) -> None:
        member_messages = await self._message_repository.with_user_id(
            user_id=notification.member_id
        )

        self._message_repository.delete_many(member_messages)
