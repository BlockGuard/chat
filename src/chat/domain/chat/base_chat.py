from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.chat_types import ChatType
from chat.domain.chat.events import ChatDeleted
from chat.domain.member.events import MemberJoinedChat
from chat.domain.member.exceptions import (
    MemberAlreadyInChatError,
    MemberNotInChatError,
    MutedMemberCantSendMessageError,
)
from chat.domain.member.member import Member
from chat.domain.member.roles import MemberRole
from chat.domain.member.statuses import MemberStatus
from chat.domain.message.message import Message
from chat.domain.message.message_id import MessageId
from chat.domain.shared.entity import Entity
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class BaseChat(Entity[ChatId]):
    def __init__(
        self,
        entity_id: ChatId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        created_at: datetime,
        chat_type: ChatType,
        members: set[Member] | None = None,
    ) -> None:
        super().__init__(entity_id, event_adder, unit_of_work)

        self._created_at = created_at
        self._chat_type = chat_type
        self._members = members or set()

    def _join_chat(
        self, member_id: UserId, current_date: datetime, role: MemberRole
    ) -> None:
        self._check_member_already_in_chat(member_id)
        member = self._create_member(member_id, role, current_date)
        member.mark_new()
        self._members.add(member)
        member.add_event(
            MemberJoinedChat(
                chat_id=self._entity_id,
                user_id=member_id,
                role=role,
                status=MemberStatus.ACTIVE,
                event_date=current_date,
            )
        )

    def _send_message(
        self,
        sender_id: UserId,
        message_id: MessageId,
        content: str,
        current_date: datetime,
    ) -> Message:
        member = self._get_validated_member(sender_id)
        self._ensure_member_not_muted(member)
        message = member.send_message(
            message_id=message_id, content=content, current_date=current_date
        )
        message.mark_new()
        return message

    def _change_member_status(
        self, member_id: UserId, status: MemberStatus, current_date: datetime
    ) -> None:
        member = self._get_validated_member(member_id)
        member.change_status(status, current_date)
        member.mark_dirty()

    def _change_member_role(
        self, member_id: UserId, role: MemberRole, current_date: datetime
    ) -> None:
        member = self._get_validated_member(member_id)
        member.change_role(role, current_date)
        member.mark_dirty()

    def _delete_chat(self, current_date: datetime) -> None:
        members_to_delete = self._members.copy()
        self._members.clear()

        for member in members_to_delete:
            member.mark_deleted()

        self.add_event(
            ChatDeleted(
                chat_id=self._entity_id,
                chat_type=self._chat_type,
                event_date=current_date,
            )
        )
        self.mark_deleted()

    def _find_member(self, member_id: UserId) -> Member | None:
        return next(
            (
                member
                for member in self._members
                if member.entity_id == member_id
            ),
            None,
        )

    def _check_member_already_in_chat(self, member_id: UserId) -> None:
        if self._find_member(member_id):
            raise MemberAlreadyInChatError(
                chat_id=self._entity_id, member_id=member_id
            )

    def _get_validated_member(self, member_id: UserId) -> Member:
        member = self._find_member(member_id)
        if not member:
            raise MemberNotInChatError(
                chat_id=self._entity_id, member_id=member_id
            )
        return member

    def _ensure_member_not_muted(self, member: Member) -> None:
        if member.status == MemberStatus.MUTED:
            raise MutedMemberCantSendMessageError(
                chat_id=self._entity_id, member_id=member.entity_id
            )

    def _create_member(
        self, member_id: UserId, role: MemberRole, current_date: datetime
    ) -> Member:
        member = Member(
            entity_id=member_id,
            event_adder=self._event_adder,
            unit_of_work=self._unit_of_work,
            chat_id=self._entity_id,
            role=role,
            joined_at=current_date,
        )
        return member

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def chat_type(self) -> ChatType:
        return self._chat_type

    @property
    def members(self) -> set[Member]:
        return self._members
