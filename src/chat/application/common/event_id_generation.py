from chat.application.common.middleware import Middleware, Then
from chat.application.ports.id_generator import IdGenerator
from chat.domain.shared.events import DomainEvent


class EventIdGenerationMiddleware(Middleware[DomainEvent, None]):
    def __init__(self, id_generator: IdGenerator) -> None:
        self._id_generator = id_generator

    async def handle(
        self,
        request: DomainEvent,
        then: Then[DomainEvent, None],
    ) -> None:
        request.set_event_id(
            self._id_generator.generate_event_id(),
        )

        await then(request)
