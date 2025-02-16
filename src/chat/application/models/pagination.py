from dataclasses import dataclass, field


@dataclass(frozen=True)
class Pagination:
    limit: int = field(default=30)
    offset: int = field(default=0)
