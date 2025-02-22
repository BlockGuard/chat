from sqlalchemy.ext.asyncio import AsyncConnection

from chat.domain.chats.chat_room import ChatRoom
from chat.infrastructure.persistence.data_mapper import DataMapper
from chat.infrastructure.persistence.sql_tables import CHATS_TABLE


class SqlChatDataMapper(DataMapper[ChatRoom]):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def insert(self, entity: ChatRoom) -> None:
        statement = CHATS_TABLE.insert().values(
            chat_id=entity.entity_id,
            created_at=entity.created_at,
        )

        await self._connection.execute(statement)

    async def delete(self, entity: ChatRoom) -> None:
        statement = CHATS_TABLE.delete().where(
            CHATS_TABLE.c.chat_id == entity.entity_id
        )

        await self._connection.execute(statement)
