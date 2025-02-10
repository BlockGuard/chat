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

from chat.domain.member.roles import MemberRole
from chat.domain.member.statuses import MemberStatus

METADATA = MetaData()

PUBLIC_CHATS_TABLE = Table(
    "public_chats",
    METADATA,
    Column("chat_id", UUID, primary_key=True),
    Column("title", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
)


PUBLIC_CHAT_MEMBERS_TABLE = Table(
    "public_chat_members",
    METADATA,
    Column("chat_id", UUID, ForeignKey("public_chats.chat_id"), primary_key=True),
    Column("user_id", UUID, primary_key=True),
    Column("role", Enum(MemberRole), nullable=False),
    Column("status", Enum(MemberStatus), nullable=False),
    Column("joined_at", DateTime(timezone=True), nullable=False),
)


PUBLIC_CHAT_MESSAGES_TABLE = Table(
    "public_chat_messages",
    METADATA,
    Column("message_id", UUID, primary_key=True),
    Column("chat_id", UUID, ForeignKey("public_chats.chat_id"), nullable=False),
    Column(
        "sender_id", UUID, ForeignKey("public_chat_members.user_id"), nullable=False
    ),
    Column("content", Text, nullable=False),
    Column("sended_at", DateTime(timezone=True), nullable=False),
    Column("edited_at", DateTime(timezone=True), nullable=True),
)
