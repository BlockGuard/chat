from abc import ABC
from typing import Any


class Request[TRes: Any](ABC): ...


class Query[TRes: Any](Request[TRes]): ...


class Command[TRes: Any](Request[TRes]): ...
