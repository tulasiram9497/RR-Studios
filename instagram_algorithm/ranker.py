from __future__ import annotations
from datetime import datetime
import math
from typing import Dict, Iterable, List
from .models import ContentItem, InteractionHistory, UserProfile, clip, get

class InstagramStyleRanker:
    """Educational Instagram-style ranking simulator, not private production code."""
    def __init__(self, half_life_hours: float = 18.0):
        self.half_life_hours = half_life_hours
        self.base_weights = {
            "watch": .25, "completion": .18, "share": .20, "save": .10,
            "like": .07, "comment": .06, "creator_affinity": .06, "topic_affinity": .08
        }

    def freshness(self, created_at: datetime | None, now: datetime) -> float:
        if created_at is None: return .5
        age_h = max(0.0, (now - created_at).total_seconds() / 3600)
        return math.exp(-math.log(2) * age_h / self.half_life_hours)

    def time_context(self, hour: int, format: str) -> float:
        # Experimental context layer; not a claim that Instagram uses fixed time weights.
        if format != "reel": return 1.0
        if 6 <= hour < 10: return 1.00
        if 18 <= hour < 23: return 1.05
        if 10 <= hour < 18: return .98
        return .92

    def score(self, user: UserProfile, history: InteractionHistory,
              item: ContentItem, now: datetime) -> Dict[str, float]:
        raw = {
            "watch": get(history.watch_ratio, item.id),
            "completion": get(history.completion_ratio, item.id),
            "share": get(history.share_rate, item.id),
            "save": get(history.save_rate, item.id),
            "like": get(history.like_rate, item.id),
            "comment": get(history.comment_rate, item.id),
            "creator_affinity": get(user.creator_affinity, item.creator_id),
            "topic_affinity": get(user.topic_affinity, item.topic),
        }
        positive = sum(self.base_weights[k] * raw[k] for k in raw)
        negative = .16 * get(history.skip_rate, item.id) + .20 * get(history.hide_rate, item.id)
        relationship = .07 if item.creator_id in user.followed_creators else 0.0
        quality_gate = .55 + .45 * clip(item.quality)
        originality = .75 + .25 * clip(item.originality)
        language = .75 + .25 * clip(item.language_match)
        fresh = self.freshness(item.created_at, now)
        context = self.time_context(now.hour, item.format)
        final = (positive - negative + relationship) * quality_gate * originality * language
        final *= (.75 + .25 * fresh) * context
        return {"id": item.id, "score": round(final, 6), "positive": round(positive, 6),
                "negative": round(negative, 6), "freshness": round(fresh, 6),
                "time_context": round(context, 6), "relationship_boost": relationship, **raw}

    def rank(self, user: UserProfile, history: InteractionHistory,
             items: Iterable[ContentItem], now: datetime, top_k: int | None = None) -> List[Dict[str, float]]:
        scored = [self.score(user, history, item, now) for item in items]
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k] if top_k else scored
