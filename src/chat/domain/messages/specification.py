from chat.domain.chats.chat_id import ChatId
from chat.domain.messages.message import Message
from chat.domain.messages.message_id import MessageId
from chat.domain.shared.specification import Specification


class ChatIdentifiedSpecification(Specification[Message]):
    def __init__(self, chat_id: ChatId) -> None:
        self._chat_id = chat_id

    def is_satisfied_by(self, candidate: Message) -> bool:
        return candidate.chat_id == self._chat_id


class MessageIdentifiedSpecification(Specification[Message]):
    def __init__(self, message_id: MessageId) -> None:
        self._message_id = message_id

    def is_satisfied_by(self, candidate: Message) -> bool:
        return candidate.entity_id == self._message_id
