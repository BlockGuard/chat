from chat.domain.chats.chat_id import ChatId
from chat.domain.chats.chat_room import ChatRoom
from chat.domain.shared.specification import Specification


class ChatIdentifiedSpecification(Specification[ChatRoom]):
    def __init__(self, chat_id: ChatId) -> None:
        self.chat_id = chat_id

    def is_satisfied_by(self, chat_room: ChatRoom) -> bool:
        return chat_room.entity_id == self.chat_id
