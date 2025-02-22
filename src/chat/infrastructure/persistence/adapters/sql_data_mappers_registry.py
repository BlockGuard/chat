from chat.domain.chats.chat_room import ChatRoom
from chat.domain.members.member import ChatMember
from chat.domain.messages.message import Message
from chat.domain.reactions.reaction import Reaction
from chat.domain.shared.entity import Entity
from chat.infrastructure.persistence.adapters.sql_chat_data_mapper import (
    SqlChatDataMapper,
)
from chat.infrastructure.persistence.adapters.sql_member_data_mapper import (
    SqlChatMemberDataMapper,
)
from chat.infrastructure.persistence.adapters.sql_message_data_mapper import (
    SqlMessageDataMapper,
)
from chat.infrastructure.persistence.adapters.sql_reaction_data_mapper import (
    SqlReactionDataMapper,
)
from chat.infrastructure.persistence.data_mapper import DataMapper
from chat.infrastructure.persistence.data_mappers_registry import (
    DataMappersRegistry,
)


class SqlDataMappersRegistry(DataMappersRegistry):
    def __init__(
        self,
        chat_data_mapper: SqlChatDataMapper,
        message_data_mapper: SqlMessageDataMapper,
        reaction_data_mapper: SqlReactionDataMapper,
        member_data_mapper: SqlChatMemberDataMapper,
    ) -> None:
        self._data_mappers_map: dict[type[Entity], DataMapper] = {
            ChatRoom: chat_data_mapper,
            Message: message_data_mapper,
            Reaction: reaction_data_mapper,
            ChatMember: member_data_mapper,
        }

    def get_mapper[EntityT: Entity](
        self, entity: type[EntityT]
    ) -> DataMapper[EntityT]:
        mapper = self._data_mappers_map.get(entity)

        if not mapper:
            raise KeyError(f"DataMapper for {entity.__name__!r} not registered")

        return mapper
