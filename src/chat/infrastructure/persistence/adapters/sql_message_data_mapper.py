from sqlalchemy.ext.asyncio import AsyncConnection

from chat.domain.messages.message import Message
from chat.infrastructure.persistence.data_mapper import DataMapper
from chat.infrastructure.persistence.sql_tables import MESSAGES_TABLE


class SqlMessageDataMapper(DataMapper[Message]):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def insert(self, entity: Message) -> None:
        statement = MESSAGES_TABLE.insert().values(
            message_id=entity.entity_id,
            sender_id=entity.sender_id,
            chat_id=entity.chat_id,
            content=entity.text,
            sent_at=entity.sent_at,
            edited_at=entity.edited_at,
        )

        await self._connection.execute(statement)

    async def update(self, entity: Message) -> None:
        statement = (
            MESSAGES_TABLE.update()
            .values(
                content=entity.text,
                edited_at=entity.edited_at,
            )
            .where(MESSAGES_TABLE.c.message_id == entity.entity_id)
        )

        await self._connection.execute(statement)

    async def delete(self, entity: Message) -> None:
        statement = MESSAGES_TABLE.delete().where(
            MESSAGES_TABLE.c.message_id == entity.entity_id
        )

        await self._connection.execute(statement)
