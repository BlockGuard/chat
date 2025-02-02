from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.chat.chat_types import ChatType
from chat.domain.chat.events import ChatDescriptionChanged, ChatTitleChanged
from chat.domain.member.events import MemberJoined
from chat.domain.member.member import Member
from chat.domain.member.roles import MemberRole
from chat.domain.shared.entity import Entity
from chat.domain.shared.events import DomainEventAdder
from chat.domain.shared.unit_of_work import UnitOfWork
from chat.domain.shared.user_id import UserId


class Chat(Entity[ChatId]):
    def __init__(
        self,
        entity_id: ChatId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        owner_id: UserId,
        created_at: datetime,
        chat_type: ChatType,
        title: str | None = None,
        description: str | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        super().__init__(entity_id, event_adder, unit_of_work)

        self._owner_id = owner_id
        self._title = title
        self._description = description
        self._updated_at = updated_at
        self._created_at = created_at
        self._chat_type = chat_type

    def edit_chat(self, title: str, description: str, current_time: datetime) -> None:
        self.edit_title(title, current_time)
        self.edit_description(description, current_time)

    def edit_title(self, title: str, current_time: datetime) -> None:
        self._title = title
        self._updated_at = current_time

        self.add_event(
            ChatTitleChanged(
                chat_id=self.entity_id,
                owner_id=self._owner_id,
                title=title,
                event_date=current_time,
            )
        )
        self.mark_dirty()

    def edit_description(self, description: str, current_time: datetime) -> None:
        self._description = description
        self._updated_at = current_time

        self.add_event(
            ChatDescriptionChanged(
                chat_id=self.entity_id,
                owner_id=self._owner_id,
                description=description,
                event_date=current_time,
            )
        )
        self.mark_dirty()

    def join_member(
        self, member_id: UserId, current_date: datetime, role: MemberRole
    ) -> None:
        member = Member(
            entity_id=member_id,
            event_adder=self._event_adder,
            unit_of_work=self._unit_of_work,
            chat_id=self.entity_id,
            role=role,
            joined_at=current_date,
        )
        member.add_event(
            MemberJoined(
                member_id=member.entity_id,
                chat_id=self.entity_id,
                role=role,
                event_date=current_date,
            )
        )
        member.mark_new()

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def owner_id(self) -> UserId:
        return self._owner_id

    @property
    def title(self) -> str | None:
        return self._title

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at

    @property
    def chat_type(self) -> ChatType:
        return self._chat_type
