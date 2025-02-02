from enum import Enum


class MemberRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    OWNER = "owner"
