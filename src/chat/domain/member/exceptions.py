from chat.domain.chat.chat_id import ChatId
from chat.domain.shared.exceptions import DomainError
from chat.domain.shared.user_id import UserId


class MemberAlreadyInChatError(DomainError):
    def __init__(self, chat_id: ChatId, member_id: UserId) -> None:
        DomainError.__init__(
            self=self,
            message=f"Member {member_id} already in chat {chat_id}",
        )


class MemberNotInChatError(DomainError):
    def __init__(self, chat_id: ChatId, member_id: UserId) -> None:
        DomainError.__init__(
            self=self,
            message=f"Member {member_id} not in chat {chat_id}",
        )


class MutedMemberCantSendMessageError(DomainError):
    def __init__(self, chat_id: ChatId, member_id: UserId) -> None:
        DomainError.__init__(
            self=self,
            message=f"Member {member_id} in chat {chat_id} is muted",
        )


class MemberHavenotPermissionError(DomainError):
    def __init__(self, chat_id: ChatId, member_id: UserId) -> None:
        DomainError.__init__(
            self=self,
            message=f"Member {member_id} have no permission",
        )
