# People Pipeline — DESIGN

## Overview
A credibility-weighted knowledge pipeline. Insights from ranked people are weighted by their tier (S/A/B/C) so we know how much to trust each piece of knowledge.

## Core Idea
```
Person Rank (S/A/B/C)
       ↓
Scrape person's content (Twitter, YouTube, etc.)
       ↓
Extract insights
       ↓
Weight by tier → credibility_score = base_score × tier_weight
       ↓
Validate: track predictions → did they come true?
       ↓
Pages with tier-weighted credibility metadata
```

## Architecture

### Pipeline Scripts

```
pipelines/people/
├── leaderboard.yaml       # Tier-ranked list of people + sources
├── ingest.py             # Main: scrape → extract → create pages
├── scorer.py             # Weight insights by tier + engagement
├── validator.py          # Track predictions → check outcomes
├── tracker.py            # Track what's been scraped per person
└── DESIGN.md
```

### How ingest.py Works

1. Load `leaderboard.yaml`
2. For each person, check `tracker.py` for last scraped timestamp
3. Scrape from their sources (Twitter via API, YouTube via existing extraction dir)
4. Extract key claims/predictions from content
5. Score each insight: `base_score × tier_weight × engagement_multiplier`
6. Create pages in `sections/people/{person_slug}/`
7. Call `rebuild_index.py`

### Page Structure

Each page from a person gets extra metadata:

```yaml
---
id: p_XXXX
book_id: b_XXXX
shelf: sections/people/jensen-huang
title: GPU scarcity will last through 2025
creator: Jensen Huang (Tier S)
source: twitter
source_url: https://twitter.com/jensen_xai/status/xxx
tier: S
tier_weight: 4.0
credibility_score: 8.5  # score × tier_weight
prediction: true         # is this a prediction?
prediction_deadline: 2025-12-31  # when to validate
validated: null         # null = unvalidated, true = confirmed, false = contradicted
links_to: []
contradicts: null
extracted_at: 2026-03-21
---
# GPU scarcity will last through 2025

**Claim**: GPU scarcity will last through 2025
**Credibility**: Tier S (Jensen Huang, NVIDIA CEO) × engagement = 8.5/10
**Prediction**: Deadline 2025-12-31 — will be validated after that date

**Why it matters**: If true, affects AI infrastructure planning globally.

**Source**: Jensen Huang via Twitter — [link]
```

### Prediction Validation

The `validator.py` script:
1. Finds all pages marked `prediction: true`
2. Checks if deadline has passed
3. Researches whether the prediction came true
4. Updates `validated: true/false/null`
5. Pages with `validated: false` are flagged as "incorrect predictions"

This lets the library track which high-tier people have the best track record.

### Output Section

Pages go into `sections/people/`:
```
sections/people/
├── jensen-huang/
│   ├── shelf.yaml
│   ├── pages/
│   │   ├── p_XXXX.md
│   │   └── ...
├── sam-altman/
├── elon-musk/
└── ...
```

## Comparison to Existing Pipelines

| Aspect | YouTube/Twitter/Reddit | People Pipeline |
|--------|------------------------|-----------------|
| Source | Platform content | Named individual |
| Credibility | Tier A/B/C from engagement | Tier S/A/B/C from leaderboard |
| Validation | None | Track predictions + outcomes |
| Routing | Topic shelf | Person shelf |

## Key Differences

1. **Person shelf** — pages are organized by who said them, not just topic
2. **Credibility score** — pages carry the tier weight in metadata
3. **Prediction tracking** — we can validate predictions over time
4. **Cross-person comparison** — compare what Jensen vs Sam say on same topic

## TODO

- [ ] `ingest.py` — scrape Twitter for listed people
- [ ] `scorer.py` — weight by tier
- [ ] `validator.py` — track predictions
- [ ] Create `sections/people/` section with bookcases
- [ ] Wire into `pipelines/shared/run.sh`
- [ ] Test with 3 people (Jensen, Sam, Elon)
