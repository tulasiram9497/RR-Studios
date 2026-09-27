from datetime import datetime, timedelta
from instagram_algorithm import ContentItem, InteractionHistory, InstagramStyleRanker, UserProfile

now = datetime(2026, 9, 28, 19, 30)
user = UserProfile(id="user-01", followed_creators={"ram"},
    topic_affinity={"ai": .95, "coding": .75, "fitness": .25},
    creator_affinity={"ram": .80, "creator-b": .40, "creator-c": .15})
items = [
    ContentItem("reel-1", "ram", "ai", quality=.9, originality=.95, created_at=now-timedelta(hours=1)),
    ContentItem("reel-2", "creator-b", "coding", quality=.85, originality=.80, created_at=now-timedelta(hours=4)),
    ContentItem("reel-3", "creator-c", "fitness", quality=.95, originality=.90, created_at=now-timedelta(hours=2)),
]
history = InteractionHistory(
    watch_ratio={"reel-1":.90,"reel-2":.70,"reel-3":.55},
    completion_ratio={"reel-1":.85,"reel-2":.60,"reel-3":.40},
    like_rate={"reel-1":.80,"reel-2":.50,"reel-3":.30},
    comment_rate={"reel-1":.45,"reel-2":.25,"reel-3":.10},
    share_rate={"reel-1":.75,"reel-2":.35,"reel-3":.08},
    save_rate={"reel-1":.60,"reel-2":.30,"reel-3":.10},
    skip_rate={"reel-1":.03,"reel-2":.12,"reel-3":.25})
for row in InstagramStyleRanker().rank(user, history, items, now):
    print(row)
