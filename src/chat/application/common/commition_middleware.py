from chat.application.common.markers import Command
from chat.application.common.middleware import Middleware, Then
from chat.application.ports.committer import Committer


class CommitionMiddleware[CommandT: Command, Result](
    Middleware[CommandT, Result]
):
    def __init__(self, committer: Committer) -> None:
        self._committer = committer

    async def handle(
        self, request: CommandT, then: Then[CommandT, Result]
    ) -> Result:
        response = await then(request)

        await self._committer.commit()

        return response
