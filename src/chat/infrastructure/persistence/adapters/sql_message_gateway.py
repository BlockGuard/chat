from collections.abc import Iterable
from typing import TYPE_CHECKING

from sqlalchemy import CursorResult, select
from sqlalchemy.ext.asyncio import AsyncConnection

from chat.application.models.message import MessageReadModel
from chat.application.models.pagination import Pagination
from chat.application.models.reaction import ReactionReadModel
from chat.application.ports.message_gateway import MessageGateway
from chat.domain.chats.chat_id import ChatId
from chat.infrastructure.persistence.sql_tables import (
    MESSAGES_TABLE,
    REACTIONS_TABLE,
)

if TYPE_CHECKING:
    from chat.domain.messages.message_id import MessageId


class SqlMessageGateway(MessageGateway):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def with_chat_id(
        self,
        chat_id: ChatId,
        pagination: Pagination,
    ) -> Iterable[MessageReadModel]:
        statement = (
            select(
                MESSAGES_TABLE.c.message_id.label("message_id"),
                MESSAGES_TABLE.c.chat_id.label("chat_id"),
                MESSAGES_TABLE.c.sender_id.label("sender_id"),
                MESSAGES_TABLE.c.content.label("content"),
                MESSAGES_TABLE.c.sent_at.label("sent_at"),
                MESSAGES_TABLE.c.edited_at.label("edited_at"),
                REACTIONS_TABLE.c.reaction_id.label("reaction_id"),
                REACTIONS_TABLE.c.owner_id.label("owner_id"),
                REACTIONS_TABLE.c.content.label("content"),
                REACTIONS_TABLE.c.set_at.label("set_at"),
            )
            .join(
                REACTIONS_TABLE,
                isouter=True,
                onclause=(
                    REACTIONS_TABLE.c.message_id == MESSAGES_TABLE.c.message_id
                ),
            )
            .where(MESSAGES_TABLE.c.chat_id == chat_id)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )

        cursor_result = await self._connection.execute(statement)
        return self._load(cursor_result)

    def _load(
        self,
        cursor_result: CursorResult,
    ) -> Iterable[MessageReadModel]:
        rows = cursor_result.all()
        messages_map: dict[MessageId, MessageReadModel] = {}

        for row in rows:
            if row.message_id not in messages_map:
                messages_map[row.message_id] = MessageReadModel(
                    message_id=row.message_id,
                    chat_id=row.chat_id,
                    user_id=row.user_id,
                    content=row.content,
                    sent_at=row.sent_at,
                    edited_at=row.edited_at,
                    reactions=set(),
                )

            if row.reaction_id:
                messages_map[row.message_id].reactions.add(
                    ReactionReadModel(
                        reaction_id=row.reaction_id,
                        message_id=row.message_id,
                        user_id=row.user_id,
                        content=row.content,
                        set_at=row.set_at,
                    )
                )

        return list(messages_map.values())
