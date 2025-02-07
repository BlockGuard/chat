from chat.domain.chat.chat_id import ChatId
from chat.domain.shared.exceptions import DomainError


class OnlyTwoMembersAllowedForPrivateChatError(DomainError):
    def __init__(self, chat_id: ChatId) -> None:
        DomainError.__init__(
            self, f"Private chat {chat_id} already has two members"
        )
