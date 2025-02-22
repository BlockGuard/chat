from sqlalchemy.ext.asyncio import AsyncConnection

from chat.domain.members.member import ChatMember
from chat.infrastructure.persistence.data_mapper import DataMapper
from chat.infrastructure.persistence.sql_tables import (
    CHAT_MEMBERS_TABLE,
)


class SqlChatMemberDataMapper(DataMapper[ChatMember]):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def insert(self, entity: ChatMember) -> None:
        statement = CHAT_MEMBERS_TABLE.insert().values(
            chat_id=entity.chat_id,
            user_id=entity.entity_id,
            status=entity.status,
            joined_at=entity.joined_at,
        )

        await self._connection.execute(statement)

    async def update(self, entity: ChatMember) -> None:
        statement = (
            CHAT_MEMBERS_TABLE.update()
            .values(status=entity.status)
            .where(CHAT_MEMBERS_TABLE.c.user_id == entity.entity_id)
        )

        await self._connection.execute(statement)

    async def delete(self, entity: ChatMember) -> None:
        statement = CHAT_MEMBERS_TABLE.delete().where(
            CHAT_MEMBERS_TABLE.c.user_id == entity.entity_id
        )

        await self._connection.execute(statement)
