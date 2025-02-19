from abc import ABC, abstractmethod
from collections.abc import Callable, Coroutine
from typing import Any, TypeVar

TRes = TypeVar("TRes")
TReq = TypeVar("TReq")


type Then[TReq, TRes] = Callable[[TReq], Coroutine[Any, Any, TRes]]


class Middleware[TReq, TRes](ABC):
    @abstractmethod
    async def handle(
        self,
        request: TReq,
        then: Then[TReq, TRes],
    ) -> TRes: ...
