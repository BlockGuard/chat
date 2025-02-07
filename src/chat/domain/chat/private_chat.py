from datetime import datetime

from chat.domain.chat.base_chat import BaseChat
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.chat_types import ChatType
from chat.domain.chat.exceptions import OnlyTwoMembersAllowedForPrivateChatError
from chat.domain.member.member import Member
from chat.domain.member.roles import MemberRole
from chat.domain.member.statuses import MemberStatus
from chat.domain.message.message import Message
from chat.domain.message.message_id import MessageId
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class PrivateChat(BaseChat):
    def __init__(
        self,
        entity_id: ChatId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        created_at: datetime,
        chat_type: ChatType = ChatType.PRIVATE,
        members: set[Member] | None = None,
    ) -> None:
        super().__init__(
            entity_id=entity_id,
            event_adder=event_adder,
            unit_of_work=unit_of_work,
            created_at=created_at,
            chat_type=chat_type,
            members=members,
        )

    def join_private_chat(
        self, member_id: UserId, current_date: datetime
    ) -> None:
        self._ensure_only_two_members()
        self._join_chat(
            member_id=member_id,
            current_date=current_date,
            role=MemberRole.OWNER,
        )

    def send_message_to_private_chat(
        self,
        sender_id: UserId,
        message_id: MessageId,
        content: str,
        current_date: datetime,
    ) -> Message:
        return self._send_message(
            sender_id=sender_id,
            message_id=message_id,
            content=content,
            current_date=current_date,
        )

    def mute_member(
        self, member_id: UserId, muter_by_id: UserId, current_date: datetime
    ) -> None:
        self._get_validated_member(muter_by_id)
        self._change_member_status(
            member_id=member_id,
            status=MemberStatus.MUTED,
            current_date=current_date,
        )

    def unmute_member(self, member_id: UserId, current_date: datetime) -> None:
        self._get_validated_member(member_id)
        self._change_member_status(
            member_id=member_id,
            status=MemberStatus.ACTIVE,
            current_date=current_date,
        )

    def delete_private_chat(
        self, deleter_id: UserId, current_date: datetime
    ) -> None:
        if self._get_validated_member(deleter_id):
            self._delete_chat(current_date)

    def _ensure_only_two_members(self) -> None:
        if len(self._members) == 2:
            raise OnlyTwoMembersAllowedForPrivateChatError(self._entity_id)
