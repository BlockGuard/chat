from datetime import datetime

from chat.domain.chat.chat_id import ChatId
from chat.domain.member.member import Member
from chat.domain.member.repository import MemberRepository
from chat.domain.member.roles import MemberRole


class RightsTransferService:
    def __init__(self, member_repository: MemberRepository) -> None:
        self._member_repository = member_repository

    async def transfer_owner_rights(
        self, chat_id: ChatId, current_date: datetime
    ) -> None:
        chat_members = await self._member_repository.with_chat_id(chat_id)

        sorted_members = self._sort_by_joined_time(chat_members)
        first_joined_member = sorted_members[1]

        first_joined_member.change_role(role=MemberRole.OWNER, current_date=current_date)

    def _sort_by_joined_time(self, members: list[Member]) -> list[Member]:
        return sorted(members, key=lambda member: member.joined_at, reverse=True)
