from enum import Enum


class MemberRole(str, Enum):
    MEMBER = "member"
    OWNER = "owner"
