from chat.application.ports.id_generator import IdGenerator
from chat.application.ports.time_provider import TimeProvider
from chat.domain.chats.chat_room import ChatRoom
from chat.domain.chats.events import ChatRoomCreated
from chat.domain.chats.factory import ChatFactory
from chat.domain.members.members_collection import MemberCollection
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork


class PostFactoryImpl(ChatFactory):
    def __init__(
        self,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        time_provider: TimeProvider,
        domain_event_adder: DomainEventAdder,
    ) -> None:
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._time_provider = time_provider
        self._domain_event_adder = domain_event_adder

    def create_chat_room(self) -> ChatRoom:
        chat_room = ChatRoom(
            entity_id=self._id_generator.generate_chat_id(),
            unit_of_work=self._unit_of_work,
            event_adder=self._domain_event_adder,
            members=MemberCollection(),
            created_at=self._time_provider.provide_current(),
        )
        event = ChatRoomCreated(
            chat_id=chat_room.entity_id,
            event_date=self._time_provider.provide_current(),
        )

        chat_room.add_event(event)

        return chat_room
