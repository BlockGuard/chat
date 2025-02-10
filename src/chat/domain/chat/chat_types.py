from enum import Enum


class ChatType(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"
