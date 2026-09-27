# Instagram Algorithm Simulator

Research-backed educational simulator of an Instagram-style recommendation/ranking pipeline.

**This is not Instagram's private production algorithm.** Meta does not publish the complete production formula or exact model weights. The project separates public platform descriptions from explicit modelling assumptions.

## Pipeline

user events -> feature aggregation -> candidate score -> context/freshness -> quality/originality gates -> ranked feed

### User inputs
- watch ratio and completion
- likes, comments, shares/sends, saves
- skips and negative feedback
- creator affinity and follows
- topic affinity
- content quality/originality/language match
- content age

### Morning vs evening
The code includes a **time-context experiment** so you can test different session assumptions. It does not claim that Instagram has a fixed morning/evening multiplier. Real production systems can learn from historical behavior and context rather than using a simple clock rule.

### Why these signals?
Meta has publicly described recommendation systems as predicting multiple possible actions/value signals and combining them. Meta has also discussed Reels watch-time measures, original-content recommendations, and sharing through messaging.

Sources:
- https://about.fb.com/news/2023/06/how-ai-ranks-content-on-facebook-and-instagram/
- https://about.fb.com/news/2023/04/instagram-reels-trending-audio-and-gifts-updates/
- https://about.fb.com/news/2025/09/in-india-instagram-debuts-a-reels-first-experience-for-its-mobile-app/
- https://about.fb.com/news/2026/01/2026-ai-drives-performance/

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest
python examples/demo.py
```

## Next upgrade
Feed the simulator real creator analytics exports, fit/calibrate the weights on observed outcomes, then compare predicted vs actual reach/watch-time/engagement.