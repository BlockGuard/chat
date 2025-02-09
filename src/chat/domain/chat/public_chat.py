import secrets
from datetime import datetime

from chat.domain.chat.base_chat import BaseChat
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.chat_types import ChatType
from chat.domain.chat.events import (
    PublicChatDescriptionEdited,
    PublicChatTitleEdited,
)
from chat.domain.member.events import MemberLeftChat
from chat.domain.member.exceptions import MemberHavenotPermissionError
from chat.domain.member.member import Member
from chat.domain.member.roles import MemberRole
from chat.domain.member.statuses import MemberStatus
from chat.domain.message.message import Message
from chat.domain.message.message_id import MessageId
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class PublicChat(BaseChat):
    def __init__(
        self,
        entity_id: ChatId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        created_at: datetime,
        chat_type: ChatType = ChatType.PUBLIC,
        members: set[Member] | None = None,
        title: str | None = None,
        description: str | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        super().__init__(
            entity_id=entity_id,
            event_adder=event_adder,
            unit_of_work=unit_of_work,
            created_at=created_at,
            chat_type=chat_type,
            members=members,
        )

        self._title = title
        self._description = description
        self._updated_at = updated_at

    def edit_description(
        self,
        description: str | None,
        current_date: datetime,
        editor_id: UserId,
    ) -> None:
        editor = self._get_validated_member(editor_id)
        self._ensure_member_have_permission(editor)
        self._description = description
        self._updated_at = current_date
        self.add_event(
            PublicChatDescriptionEdited(
                chat_id=self.entity_id,
                chat_type=self._chat_type,
                description=self._description,
                event_date=current_date,
            )
        )
        self.mark_dirty()

    def edit_title(
        self, title: str | None, current_date: datetime, editor_id: UserId
    ) -> None:
        editor = self._get_validated_member(editor_id)
        self._ensure_member_have_permission(editor)
        self._title = title
        self._updated_at = current_date
        self.add_event(
            PublicChatTitleEdited(
                chat_id=self.entity_id,
                chat_type=self._chat_type,
                title=self._title,
                event_date=current_date,
            )
        )
        self.mark_dirty()

    def join_public_chat(
        self, member_id: UserId, current_date: datetime, role: MemberRole
    ) -> None:
        self._join_chat(member_id, current_date, role)

    def leave_public_chat(self, member_id: UserId, current_date: datetime) -> None:
        if len(self.members) == 1:
            self._delete_chat(current_date)
            return

        member = self._get_validated_member(member_id)

        if member.role == MemberRole.OWNER:
            self._transfer_ownership(current_date)

        self._members.remove(member)
        member.mark_deleted()
        member.add_event(
            MemberLeftChat(
                chat_id=self.entity_id,
                user_id=member_id,
                event_date=current_date,
            )
        )

    def kick_member(
        self,
        kicked_by_id: UserId,
        member_id: UserId,
        current_date: datetime,
    ) -> None:
        kicked_by = self._get_validated_member(kicked_by_id)
        member = self._get_validated_member(member_id)
        self._ensure_member_have_permission(kicked_by)
        self._members.remove(member)
        member.mark_deleted()
        member.add_event(
            MemberLeftChat(
                chat_id=self.entity_id,
                user_id=member_id,
                event_date=current_date,
            )
        )

    def change_member_status(
        self,
        member_id: UserId,
        status: MemberStatus,
        changed_by_id: UserId,
        current_date: datetime,
    ) -> None:
        changed_by = self._get_validated_member(changed_by_id)
        self._ensure_member_have_permission(changed_by)
        self._change_member_status(
            member_id=member_id, status=status, current_date=current_date
        )

    def delete_public_chat(self, member_id: UserId, current_date: datetime) -> None:
        member = self._get_validated_member(member_id)
        self._ensure_member_have_permission(member)
        self._delete_chat(current_date)

    def send_message_to_public_chat(
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

    def _transfer_ownership(self, current_date: datetime) -> None:
        members_list = list(self._members)
        new_owner = members_list[secrets.randbelow(len(members_list))]
        self._change_member_role(
            member_id=new_owner.entity_id,
            role=MemberRole.OWNER,
            current_date=current_date,
        )

    def _ensure_member_have_permission(self, member: Member) -> None:
        if member.role == MemberRole.MEMBER:
            raise MemberHavenotPermissionError(self._entity_id, member.entity_id)

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def title(self) -> str | None:
        return self._title

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at
