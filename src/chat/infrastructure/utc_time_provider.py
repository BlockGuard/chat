from datetime import UTC, datetime

from chat.application.ports.time_provider import TimeProvider


class UtcTimeProvider(TimeProvider):
    def provide_current(self) -> datetime:
        return datetime.now(UTC)
