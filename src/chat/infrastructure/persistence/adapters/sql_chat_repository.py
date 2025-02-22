from sqlalchemy import CursorResult, select
from sqlalchemy.ext.asyncio import AsyncConnection

from chat.domain.chats.chat_id import ChatId
from chat.domain.chats.chat_room import ChatRoom
from chat.domain.chats.repository import ChatRepository
from chat.domain.members.member import ChatMember
from chat.domain.members.members_collection import MemberCollection
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.infrastructure.persistence.sql_tables import (
    CHAT_MEMBERS_TABLE,
    CHATS_TABLE,
)


class SqlChatRepository(ChatRepository):
    def __init__(
        self,
        connection: AsyncConnection,
        unit_of_work: UnitOfWork,
        event_adder: DomainEventAdder,
    ) -> None:
        self._connection = connection
        self._unit_of_work = unit_of_work
        self._event_adder = event_adder
        self._identity_map: dict[ChatId, ChatRoom] = {}

    def add(self, chat_room: ChatRoom) -> None:
        self._unit_of_work.register_new(chat_room)
        self._identity_map[chat_room.entity_id] = chat_room

    def delete(self, chat_room: ChatRoom) -> None:
        self._unit_of_work.register_deleted(chat_room)
        self._identity_map.pop(chat_room.entity_id)

    async def with_chat_id(self, chat_id: ChatId) -> ChatRoom | None:
        if chat_id in self._identity_map:
            return self._identity_map[chat_id]

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

    def _load(self, cursor_result: CursorResult) -> ChatRoom | None:
        chat_row = cursor_result.one_or_none()

        if not chat_row:
            return None

        members = MemberCollection()
        chat_room = ChatRoom(
            unit_of_work=self._unit_of_work,
            event_adder=self._event_adder,
            entity_id=chat_row.chat_id,
            created_at=chat_row.created_at,
            members=members,
        )

        for member_row in cursor_result.all():
            members.add(
                ChatMember(
                    unit_of_work=self._unit_of_work,
                    event_adder=self._event_adder,
                    chat_id=chat_row.chat_id,
                    entity_id=member_row.user_id,
                    joined_at=member_row.joined_at,
                    status=member_row.status,
                )
            )

        return chat_room
