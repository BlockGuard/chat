from collections.abc import Iterable

from sqlalchemy import CursorResult, select
from sqlalchemy.ext.asyncio import AsyncConnection

from chat.application.models.chat import ChatReadModel
from chat.application.models.member import ChatMemberReadModel
from chat.application.models.pagination import Pagination
from chat.application.ports.chat_gateway import ChatGateway
from chat.domain.chats.chat_id import ChatId
from chat.domain.shared.user_id import UserId
from chat.infrastructure.persistence.sql_tables import (
    CHAT_MEMBERS_TABLE,
    CHATS_TABLE,
)


class SqlChatGateway(ChatGateway):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def with_chat_id(self, chat_id: ChatId) -> ChatReadModel | None:
        statement = (
            select(
                CHATS_TABLE.c.chat_id.label("chat_id"),
                CHATS_TABLE.c.created_at.label("created_at"),
                CHAT_MEMBERS_TABLE.c.user_id.label("user_id"),
                CHAT_MEMBERS_TABLE.c.joined_at.label("joined_at"),
                CHAT_MEMBERS_TABLE.c.status.label("status"),
            )
            .join(CHAT_MEMBERS_TABLE, isouter=True)
            .where(CHATS_TABLE.c.chat_id == chat_id)
        )
        cursor_result = await self._connection.execute(statement)

        return self._load(cursor_result)

    async def with_user_id(
        self, user_id: UserId, pagination: Pagination
    ) -> Iterable[ChatReadModel]:
        statement = (
            select(
                CHATS_TABLE.c.chat_id.label("chat_id"),
                CHATS_TABLE.c.created_at.label("created_at"),
                CHAT_MEMBERS_TABLE.c.user_id.label("user_id"),
                CHAT_MEMBERS_TABLE.c.joined_at.label("joined_at"),
                CHAT_MEMBERS_TABLE.c.status.label("status"),
            )
            .join(CHAT_MEMBERS_TABLE, isouter=True)
            .where(CHAT_MEMBERS_TABLE.c.user_id == user_id)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        cursor_result = await self._connection.execute(statement)

        return self._load_many(cursor_result)

    def _load_many(
        self, cursor_result: CursorResult
    ) -> Iterable[ChatReadModel]:
        rows = cursor_result.all()

        unique_chat_ids = {row.chat_id for row in rows}

        return [
            ChatReadModel(
                chat_id=chat_id,
                created_at=next(
                    row.created_at for row in rows if row.chat_id == chat_id
                ),
                members=[
                    ChatMemberReadModel(
                        chat_id=row.chat_id,
                        user_id=row.user_id,
                        joined_at=row.joined_at,
                        status=row.status,
                    )
                    for row in rows
                    if row.chat_id == chat_id and row.user_id is not None
                ],
            )
            for chat_id in unique_chat_ids
        ]

    def _load(self, cursor_result: CursorResult) -> ChatReadModel | None:
        chat_row = cursor_result.one_or_none()

        if not chat_row:
            return None

        members: set[ChatMemberReadModel] = set()
        chat_room = ChatReadModel(
            chat_id=chat_row.chat_id,
            created_at=chat_row.created_at,
            members=members,
        )

        for member_row in cursor_result.all():
            if member_row.user_id is not None:
                members.add(
                    ChatMemberReadModel(
                        chat_id=member_row.chat_id,
                        user_id=member_row.user_id,
                        joined_at=member_row.joined_at,
                        status=member_row.status,
                    )
                )

        return chat_room
