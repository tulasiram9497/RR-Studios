from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Set

@dataclass(frozen=True)
class ContentItem:
    id: str
    creator_id: str
    topic: str
    format: str = "reel"
    duration_s: float = 30.0
    quality: float = 0.7
    originality: float = 0.8
    language_match: float = 1.0
    created_at: datetime | None = None

@dataclass
class UserProfile:
    id: str
    followed_creators: Set[str] = field(default_factory=set)
    topic_affinity: Dict[str, float] = field(default_factory=dict)
    creator_affinity: Dict[str, float] = field(default_factory=dict)

@dataclass
class InteractionHistory:
    watch_ratio: Dict[str, float] = field(default_factory=dict)
    completion_ratio: Dict[str, float] = field(default_factory=dict)
    like_rate: Dict[str, float] = field(default_factory=dict)
    comment_rate: Dict[str, float] = field(default_factory=dict)
    share_rate: Dict[str, float] = field(default_factory=dict)
    save_rate: Dict[str, float] = field(default_factory=dict)
    profile_visit_rate: Dict[str, float] = field(default_factory=dict)
    follow_rate: Dict[str, float] = field(default_factory=dict)
    skip_rate: Dict[str, float] = field(default_factory=dict)
    hide_rate: Dict[str, float] = field(default_factory=dict)

def clip(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))

def get(mapping: Dict[str, float], key: str, default: float = 0.0) -> float:
    return clip(mapping.get(key, default))
