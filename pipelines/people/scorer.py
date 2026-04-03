#!/usr/bin/env python3
"""
Score people and update tiers based on follower_count and prediction_accuracy.

Tier thresholds:
- S: 50000+ followers OR (25000+ AND prediction_accuracy > 70%)
- A: 10000+ followers
- B: 1000+ followers
- C: <1000 followers

Usage:
    python3 pipelines/people/scorer.py
    python3 pipelines/people/scorer.py --dry-run
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Library")
LEADERBOARD_FILE = ROOT / "pipelines" / "people" / "leaderboard.yaml"
PROFILE_SHELF = ROOT / "sections" / "people" / "bookcases" / "people" / "shelves" / "intelligence" / "pages"


def load_leaderboard() -> list[dict]:
    import yaml
    with open(LEADERBOARD_FILE) as f:
        data = yaml.safe_load(f)
    return data.get("people", [])


def save_leaderboard(people: list[dict]):
    import yaml
    with open(LEADERBOARD_FILE, "w") as f:
        yaml.dump({"people": people}, f, default_flow_style=False, sort_keys=False)


def compute_tier(follower_count: int, prediction_accuracy: float | None) -> str:
    """Compute tier based on follower count and prediction accuracy."""
    if follower_count >= 50000:
        return "S"
    if follower_count >= 25000 and prediction_accuracy is not None and prediction_accuracy > 70:
        return "S"
    if follower_count >= 10000:
        return "A"
    if follower_count >= 1000:
        return "B"
    return "C"


def read_profile_page(handle: str) -> dict:
    """Read a person's profile page to extract prediction stats."""
    handle_clean = handle.lstrip("@")
    # Try to find existing profile page
    if not PROFILE_SHELF.exists():
        return {}

    for page_file in PROFILE_SHELF.glob("*.md"):
        content = page_file.read_text()
        # Check if this page belongs to the handle
        if f'handle: "{handle}"' in content or f"handle: '{handle}'" in content or f"handle: {handle}" in content:
            return parse_profile_content(content)

    return {}


def parse_profile_content(content: str) -> dict:
    """Parse prediction status from profile page content."""
    result = {
        "prediction_accuracy": None,
        "total_predictions": 0,
        "validated": 0,
        "contradicted": 0,
    }

    # Count validated/contradicted predictions
    validated_count = len(re.findall(r'\bVALIDATED\b', content, re.IGNORECASE))
    contradicted_count = len(re.findall(r'\bCONTRADICTED\b', content, re.IGNORECASE))

    result["validated"] = validated_count
    result["contradicted"] = contradicted_count
    result["total_predictions"] = validated_count + contradicted_count

    if result["total_predictions"] > 0:
        result["prediction_accuracy"] = round(
            (validated_count / result["total_predictions"]) * 100, 1
        )

    # Try to extract existing prediction_accuracy from frontmatter
    match = re.search(r'prediction_accuracy:\s*(\d+(?:\.\d+)?)', content)
    if match:
        result["prediction_accuracy"] = float(match.group(1))

    return result


def update_person_tier(person: dict, dry_run: bool = False) -> dict:
    """Update tier for a single person based on current stats."""
    handle = person["handle"]
    old_tier = person.get("tier", "C")
    follower_count = person.get("follower_count", 0)

    # Read profile to get prediction accuracy
    profile_stats = read_profile_page(handle)
    prediction_accuracy = profile_stats.get("prediction_accuracy")

    new_tier = compute_tier(follower_count, prediction_accuracy)

    if dry_run:
        print(f"  [DRY] {handle}: {old_tier} -> {new_tier} (followers={follower_count}, accuracy={prediction_accuracy}%)")
        return {**person, "tier": new_tier, "old_tier": old_tier}

    if new_tier != old_tier:
        person["tier"] = new_tier
        print(f"  {handle}: Tier {old_tier} -> {new_tier} (followers={follower_count}, accuracy={prediction_accuracy}%)")
    else:
        print(f"  {handle}: Tier unchanged {old_tier} (followers={follower_count}, accuracy={prediction_accuracy}%)")

    return person


def main():
    parser = argparse.ArgumentParser(description="Score people and update tiers")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    args = parser.parse_args()

    print("=== People Scorer ===")

    people = load_leaderboard()
    print(f"Loaded {len(people)} people from leaderboard")

    updated = []
    for person in people:
        updated_person = update_person_tier(person, dry_run=args.dry_run)
        updated.append(updated_person)

    if not args.dry_run:
        save_leaderboard(updated)
        print(f"\nUpdated leaderboard.yaml")
    else:
        print(f"\n[DRY RUN] No changes written")

    print(f"\n=== Tier Distribution ===")
    tiers = {}
    for p in updated:
        t = p.get("tier", "?")
        tiers[t] = tiers.get(t, 0) + 1
    for t in ["S", "A", "B", "C"]:
        count = tiers.get(t, 0)
        print(f"  Tier {t}: {count}")


if __name__ == "__main__":
    main()
