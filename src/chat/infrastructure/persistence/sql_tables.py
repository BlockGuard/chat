from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    MetaData,
    Table,
    Text,
)

from chat.domain.members.statuses import Status

METADATA = MetaData()

CHATS_TABLE = Table(
    "chats",
    METADATA,
    Column("chat_id", UUID(as_uuid=True), primary_key=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

CHAT_MEMBERS_TABLE = Table(
    "chat_members",
    METADATA,
    Column(
        "chat_id",
        UUID(as_uuid=True),
        ForeignKey("chats.chat_id"),
        primary_key=True,
    ),
    Column("user_id", UUID(as_uuid=True), primary_key=True),
    Column("joined_at", DateTime(timezone=True), nullable=False),
    Column("status", Enum(Status), nullable=False),
)

MESSAGES_TABLE = Table(
    "messages",
    METADATA,
    Column("message_id", UUID(as_uuid=True), primary_key=True),
    Column(
        "chat_id",
        UUID(as_uuid=True),
        ForeignKey("chats.chat_id"),
        nullable=False,
    ),
    Column(
        "sender_id",
        UUID(as_uuid=True),
        ForeignKey("chat_members.user_id"),
        nullable=False,
    ),
    Column("content", Text, nullable=False),
    Column("sent_at", DateTime(timezone=True), nullable=False),
    Column("edited_at", DateTime(timezone=True)),
)

REACTIONS_TABLE = Table(
    "reactions",
    METADATA,
    Column("reaction_id", UUID(as_uuid=True), primary_key=True),
    Column(
        "message_id",
        UUID(as_uuid=True),
        ForeignKey("messages.message_id"),
        nullable=False,
    ),
    Column(
        "owner_id",
        UUID(as_uuid=True),
        ForeignKey("chat_members.user_id"),
        nullable=False,
    ),
    Column("content", Text, nullable=False),
    Column("set_at", DateTime(timezone=True), nullable=False),
)
