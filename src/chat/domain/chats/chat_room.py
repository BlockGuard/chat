from datetime import datetime

from chat.domain.chats.chat_id import ChatId
from chat.domain.chats.exceptions import LimitOfMembersReachedError
from chat.domain.members.events import MemberJoinedChat
from chat.domain.members.member import ChatMember
from chat.domain.members.members_collection import MemberCollection
from chat.domain.members.statuses import Status
from chat.domain.messages.message import Message
from chat.domain.messages.message_id import MessageId
from chat.domain.shared.entity import Entity
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class ChatRoom(Entity[ChatId]):
    MEMBERS_LIMIT = 2

    def __init__(
        self,
        entity_id: ChatId,
        unit_of_work: UnitOfWork,
        event_adder: DomainEventAdder,
        *,
        members: MemberCollection,
        created_at: datetime,
    ) -> None:
        super().__init__(entity_id, event_adder, unit_of_work)

        self._members = members
        self._created_at = created_at

    def join_chat(
        self, member_id: UserId, current_date: datetime
    ) -> None:
        self._ensure_limit_not_reached()
        member = ChatMember(
            entity_id=member_id,
            unit_of_work=self._unit_of_work,
            event_adder=self._event_adder,
            chat_id=self._entity_id,
        )
        event = MemberJoinedChat(
            user_id=member_id,
            chat_id=self._entity_id,
            event_date=current_date,
        )
        self._members.add(member)
        self.add_event(event)
        member.mark_new()

    def send_message(
        self,
        message_id: MessageId,
        sender_id: UserId,
        content: str,
        current_date: datetime,
    ) -> Message:
        member = self._members.get(sender_id)
        message = member.send_message(
            message_id=message_id,
            content=content,
            current_date=current_date,
        )
        message.mark_new()

        return message

    def edit_member_status(
        self,
        editor_id: UserId,
        member_id: UserId,
        status: Status,
        current_date: datetime,
    ) -> None:
        editor = self._members.get(editor_id)
        editor.ensure_active()
        member = self._members.get(member_id)
        member.edit_status(status=status, current_date=current_date)
        member.mark_dirty()

    def _ensure_limit_not_reached(self) -> None:
        if self._members.count() == self.MEMBERS_LIMIT:
            raise LimitOfMembersReachedError

    def ensure_member_in_chat(self, user_id: UserId) -> None:
        self._members.get(user_id)

    @property
    def members(self) -> set[ChatMember]:
        return self._members

    @property
    def created_at(self) -> datetime:
        return self._created_at
