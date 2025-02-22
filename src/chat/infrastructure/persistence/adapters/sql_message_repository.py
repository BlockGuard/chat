from sqlalchemy import CursorResult, select
from sqlalchemy.ext.asyncio import AsyncConnection

from chat.domain.messages.message import Message
from chat.domain.messages.message_id import MessageId
from chat.domain.messages.repository import MessageRepository
from chat.domain.reactions.reaction import Reaction
from chat.domain.reactions.reactions_collection import (
    ReactionsCollection,
)
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.infrastructure.persistence.sql_tables import (
    MESSAGES_TABLE,
    REACTIONS_TABLE,
)


class SqlMessageRepository(MessageRepository):
    def __init__(
        self,
        connection: AsyncConnection,
        unit_of_work: UnitOfWork,
        event_adder: DomainEventAdder,
    ) -> None:
        self._connection = connection
        self._event_adder = event_adder
        self._unit_of_work = unit_of_work
        self._identity_map: dict[MessageId, Message] = {}

    async def with_message_id(self, message_id: MessageId) -> Message | None:
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
            )
            .where(MESSAGES_TABLE.c.message_id == message_id)
        )
        cursor_result = await self._connection.execute(statement)

        return self._load(cursor_result)

    def _load(self, cursor_result: CursorResult) -> Message | None:
        message_row = cursor_result.one_or_none()

        if not message_row:
            return None

        reactions = ReactionsCollection()
        message = Message(
            entity_id=message_row.message_id,
            unit_of_work=self._unit_of_work,
            event_adder=self._event_adder,
            sender_id=message_row.sender_id,
            chat_id=message_row.chat_id,
            text=message_row.content,
            sent_at=message_row.sent_at,
            edited_at=message_row.edited_at,
            reactions=reactions,
        )

        for reaction_row in cursor_result:
            reaction = Reaction(
                unit_of_work=self._unit_of_work,
                event_adder=self._event_adder,
                message_id=reaction_row.message_id,
                entity_id=reaction_row.reaction_id,
                user_id=reaction_row.owner_id,
                reaction=reaction_row.content,
                set_at=reaction_row.set_at,
            )
            reactions.add(reaction)

        return message
