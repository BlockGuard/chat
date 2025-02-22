from sqlalchemy.ext.asyncio import AsyncConnection

from chat.domain.reactions.reaction import Reaction
from chat.infrastructure.persistence.data_mapper import DataMapper
from chat.infrastructure.persistence.sql_tables import REACTIONS_TABLE


class SqlReactionDataMapper(DataMapper[Reaction]):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def insert(self, entity: Reaction) -> None:
        statement = REACTIONS_TABLE.insert().values(
            reaction_id=entity.entity_id,
            message_id=entity.message_id,
            owner_id=entity.user_id,
            content=entity.reaction,
            set_at=entity.set_at,
        )

        await self._connection.execute(statement)

    async def delete(self, entity: Reaction) -> None:
        statement = REACTIONS_TABLE.delete().where(
            REACTIONS_TABLE.c.reaction_id == entity.entity_id
        )

        await self._connection.execute(statement)
