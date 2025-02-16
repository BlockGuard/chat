from datetime import datetime

from chat.domain.chat.base_chat import BaseChat
from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.chat_types import ChatType
from chat.domain.chat.events import PrivateChatDeleted
from chat.domain.chat.exceptions import (
    OnlyTwoMembersAllowedForPrivateChatError,
)
from chat.domain.member.events import MemberJoinedPrivateChat
from chat.domain.member.member_collection import MemberCollection
from chat.domain.member.private_chat_member import PrivateChatMember
from chat.domain.member.statuses import MemberStatus
from chat.domain.message.message_id import MessageId
from chat.domain.message.private_chat_message import (
    PrivateChatMessage,
)
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class PrivateChat(BaseChat[PrivateChatMember]):
    def __init__(
        self,
        entity_id: ChatId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        created_at: datetime,
        chat_type: ChatType,
        members: MemberCollection[PrivateChatMember],
    ) -> None:
        BaseChat.__init__(
            self=self,
            entity_id=entity_id,
            event_adder=event_adder,
            unit_of_work=unit_of_work,
            chat_type=chat_type,
            created_at=created_at,
            members=members,
        )

    def join(
        self,
        member_id: UserId,
        current_date: datetime,
    ) -> None:
        self._enure_two_members()
        member = PrivateChatMember(
            entity_id=member_id,
            event_adder=self._event_adder,
            unit_of_work=self._unit_of_work,
            chat_id=self.entity_id,
            status=MemberStatus.ACTIVE,
            joined_at=current_date,
        )
        self._members.add(member)
        event = MemberJoinedPrivateChat(
            chat_id=self._entity_id,
            user_id=member_id,
            status=member.status,
            event_date=current_date,
        )
        member.add_event(event)
        member.mark_new()

    def send_message(
        self,
        sender_id: UserId,
        message_id: MessageId,
        content: str,
        current_date: datetime,
    ) -> PrivateChatMessage:
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
        self,
        current_date: datetime,
        deleter_id: UserId,
    ) -> None:
        self._members.get(
            member_id=deleter_id,
            chat_id=self._entity_id,
        )
        self._members.clear()
        self.add_event(
            event=PrivateChatDeleted(
                chat_id=self._entity_id,
                event_date=current_date,
            )
        )

    def _enure_two_members(self) -> None:
        if len(self._members) == 2:
            raise OnlyTwoMembersAllowedForPrivateChatError(
                chat_id=self._entity_id
            )
