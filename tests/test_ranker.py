from datetime import datetime, timedelta
from instagram_algorithm import ContentItem, InteractionHistory, InstagramStyleRanker, UserProfile

def test_high_intent_engagement_ranks_higher():
    now = datetime(2026, 9, 28, 19, 0)
    user = UserProfile(id="u", topic_affinity={"ai": 1.0}, creator_affinity={"c": .5})
    h = InteractionHistory(
        watch_ratio={"a": .9, "b": .5},
        completion_ratio={"a": .9, "b": .5},
        share_rate={"a": .9, "b": .1},
    )
    items = [
        ContentItem("a", "c", "ai", quality=.8, created_at=now),
        ContentItem("b", "c", "ai", quality=.8, created_at=now),
    ]
    assert InstagramStyleRanker().rank(user, h, items, now)[0]["id"] == "a"

def test_negative_feedback_reduces_score():
    now = datetime(2026, 9, 28, 19, 0)
    user = UserProfile(id="u", topic_affinity={"ai": .8})
    h = InteractionHistory(watch_ratio={"a": .7}, completion_ratio={"a": .7},
                           share_rate={"a": .5}, skip_rate={"a": .9}, hide_rate={"a": .8})
    row = InstagramStyleRanker().score(user, h, ContentItem("a", "c", "ai", created_at=now), now)
    assert row["negative"] > .25

def test_freshness_decays():
    ranker = InstagramStyleRanker()
    now = datetime(2026, 9, 28, 19, 0)
    assert ranker.freshness(now, now) > ranker.freshness(now - timedelta(hours=36), now)
