from datetime import datetime
from secrets import randbelow

from chat.domain.chat.base_chat import BaseChat
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.chat_types import ChatType
from chat.domain.chat.events import (
    PublicChatDeleted,
    PublicChatDescriptionEdited,
    PublicChatTitleEdited,
)
from chat.domain.member.events import (
    MemberJoinedPublicChat,
    PublicChatMemberLeftChat,
)
from chat.domain.member.exceptions import MemberHavenotPermissionError
from chat.domain.member.member_collection import MemberCollection
from chat.domain.member.public_chat_member import PublicChatMember
from chat.domain.member.roles import MemberRole
from chat.domain.member.statuses import MemberStatus
from chat.domain.message.message_id import MessageId
from chat.domain.message.public_chat_message import PublicChatMessage
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class PublicChat(BaseChat[PublicChatMember]):
    def __init__(
        self,
        entity_id: ChatId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        created_at: datetime,
        chat_type: ChatType,
        title: str | None,
        description: str | None,
        updated_at: datetime | None,
        members: MemberCollection[PublicChatMember],
    ) -> None:
        BaseChat.__init__(
            self=self,
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
        editor = self._members.get(
            member_id=editor_id, chat_id=self.entity_id
        )
        self._ensure_permissioned(editor)
        self._description = description
        self._updated_at = current_date
        event = PublicChatDescriptionEdited(
            chat_id=self.entity_id,
            description=description,
            event_date=current_date,
        )
        self.add_event(event)
        self.mark_dirty()

    def edit_title(
        self,
        title: str | None,
        current_date: datetime,
        editor_id: UserId,
    ) -> None:
        editor = self._members.get(
            member_id=editor_id, chat_id=self.entity_id
        )
        self._ensure_permissioned(editor)
        self._title = title
        self._updated_at = current_date
        events = PublicChatTitleEdited(
            chat_id=self.entity_id,
            title=title,
            event_date=current_date,
        )
        self.add_event(events)
        self.mark_dirty()

    def join(
        self,
        member_id: UserId,
        current_date: datetime,
    ) -> None:
        member = PublicChatMember(
            entity_id=member_id,
            event_adder=self._event_adder,
            unit_of_work=self._unit_of_work,
            chat_id=self.entity_id,
            status=MemberStatus.ACTIVE,
            role=(
                MemberRole.MEMBER
                if len(self._members) >= 1
                else MemberRole.OWNER
            ),
            joined_at=current_date,
        )
        self._members.add(member)
        event = MemberJoinedPublicChat(
            chat_id=self._entity_id,
            user_id=member_id,
            status=member.status,
            role=member.role,
            event_date=current_date,
        )
        member.add_event(event)
        member.mark_new()

    def leave(
        self, member_id: UserId, current_date: datetime
    ) -> None:
        member = self._members.get(
            member_id=member_id, chat_id=self.entity_id
        )
        if len(self._members) == 1:
            self._members.clear()
            chat_event = PublicChatDeleted(
                chat_id=self._entity_id, event_date=current_date
            )
            self.add_event(chat_event)
            self.mark_deleted()
            return

        if member.role == MemberRole.OWNER:
            self._transfer_ownership(current_date=current_date)

        member_event = PublicChatMemberLeftChat(
            chat_id=self._entity_id,
            user_id=member_id,
            event_date=current_date,
        )
        self._members.remove(member)
        member.add_event(member_event)
        member.mark_deleted()

    def kick_member(
        self,
        kicker_id: UserId,
        member_id: UserId,
        current_date: datetime,
    ) -> None:
        member = self._members.get(
            member_id=member_id, chat_id=self.entity_id
        )
        kicker = self._members.get(
            member_id=kicker_id, chat_id=self.entity_id
        )
        self._ensure_permissioned(kicker)
        event = PublicChatMemberLeftChat(
            chat_id=self._entity_id,
            user_id=member_id,
            event_date=current_date,
        )
        self._members.remove(member)
        member.add_event(event)
        member.mark_deleted()

    def _ensure_permissioned(self, member: PublicChatMember) -> None:
        if member.role != MemberRole.OWNER:
            raise MemberHavenotPermissionError(
                chat_id=self._entity_id, member_id=member.entity_id
            )

    def _transfer_ownership(self, current_date: datetime) -> None:
        candidates = [
            member
            for member in self._members
            if member.role == MemberRole.MEMBER
        ]
        new_owner = candidates[randbelow(len(candidates))]
        new_owner.edit_role(
            role=MemberRole.OWNER, current_date=current_date
        )
        new_owner.mark_dirty()

    def send_message(
        self,
        sender_id: UserId,
        message_id: MessageId,
        content: str,
        current_date: datetime,
    ) -> PublicChatMessage:
        sender = self._members.get(
            member_id=sender_id, chat_id=self._entity_id
        )

        message = sender.send_message(
            message_id=message_id,
            content=content,
            current_date=current_date,
        )

        return message

    def delete_chat(
        self, current_date: datetime, deleter_id: UserId
    ) -> None:
        deleter = self._members.get(
            member_id=deleter_id, chat_id=self.entity_id
        )
        self._ensure_permissioned(deleter)
        self._members.clear()
        event = PublicChatDeleted(
            chat_id=self.entity_id, event_date=current_date
        )
        self.add_event(event)

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def title(self) -> str | None:
        return self._title

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at
