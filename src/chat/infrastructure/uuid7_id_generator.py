from uuid_extensions import uuid7  # type: ignore

from chat.application.ports.id_generator import IdGenerator
from chat.domain.chats.chat_id import ChatId
from chat.domain.messages.message_id import MessageId
from chat.domain.reactions.reaction_id import ReactionId
from chat.domain.shared.event_id import EventId


class UUID7IdGenerator(IdGenerator):
    def generate_chat_id(self) -> ChatId:
        return ChatId(uuid7())

    def generate_message_id(self) -> MessageId:
        return MessageId(uuid7())

    def generate_reaction_id(self) -> ReactionId:
        return ReactionId(uuid7())

    def generate_event_id(self) -> EventId:
        return EventId(uuid7())
