"""Reference implementation of availability-time filtering."""
from dataclasses import dataclass
from datetime import datetime
from math import isfinite
from typing import Iterable


def aware(value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timezone-aware timestamp required")


@dataclass(frozen=True)
class Observation:
    entity_id: str
    feature: str
    event_at: datetime
    available_at: datetime
    ingested_at: datetime
    revision: int
    value: float

    def __post_init__(self):
        for value in (self.event_at, self.available_at, self.ingested_at):
            aware(value)
        if not isfinite(self.value) or self.revision < 0:
            raise ValueError("invalid observation")
        if self.ingested_at < self.available_at:
            raise ValueError("ingestion cannot precede availability")


def as_of(rows: Iterable[Observation], entity_id: str, feature: str,
          cutoff: datetime) -> Observation | None:
    """Latest eligible event, then latest eligible revision. Exact ties fail."""
    aware(cutoff)
    eligible = [r for r in rows if r.entity_id == entity_id and r.feature == feature
                and r.event_at < cutoff and r.available_at <= cutoff
                and r.ingested_at <= cutoff]
    if not eligible:
        return None
    key = lambda r: (r.event_at, r.available_at, r.ingested_at, r.revision)
    latest = max(eligible, key=key)
    if sum(key(r) == key(latest) for r in eligible) > 1:
        raise ValueError("ambiguous duplicate observation")
    return latest
