from enum import Enum


class Status(str, Enum):
    BLOCKED = "blocked"
    ACTIVE = "active"
