from chat.application.common.markers import Command
from chat.application.common.middleware import Middleware, Then
from chat.application.common.publisher import Publisher
from chat.application.ports.event_raiser import DomainEventsRaiser


class EventPublishingMiddleware[CommandT: Command, Result](
    Middleware[CommandT, Result]
):
    def __init__(
        self,
        publisher: Publisher,
        events_raiser: DomainEventsRaiser,
    ) -> None:
        self._publisher = publisher
        self._events_raiser = events_raiser

    async def handle(
        self, request: CommandT, then: Then[CommandT, Result]
    ) -> Result:
        response = await then(request)

        for event in self._events_raiser.raise_events():
            await self._publisher.publish(event)

        return response
