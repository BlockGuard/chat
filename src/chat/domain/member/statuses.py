from enum import Enum


class MemberStatus(str, Enum):
    ACTIVE = "active"
    MUTED = "muted"
