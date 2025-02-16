from abc import ABC, abstractmethod
from typing import Any

from chat.application.common.markers import Request
from chat.domain.shared.markers import Notification


class RequestHandler[TReq: Request, TRes: Any](ABC):
    @abstractmethod
    async def handle(self, request: TReq) -> TRes: ...


class NotificationHandler[TNot: Notification](ABC):
    @abstractmethod
    async def handle(self, notification: TNot) -> None: ...
