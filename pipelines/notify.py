#!/usr/bin/env python3
"""Notification Pipeline - Push relevant pages to subscribed agents."""
import argparse
import json
from datetime import datetime, timedelta, timezone, date
from pathlib import Path

import yaml

LIB_PATH = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
INDEX_PATH = LIB_PATH / "_index"
AGENTS_PATH = LIB_PATH / "agents"


def load_manifest() -> dict:
    """Load the page manifest."""
    manifest_path = INDEX_PATH / "_manifest.yaml"
    if not manifest_path.exists():
        return {}
    with open(manifest_path) as f:
        return yaml.safe_load(f)


def get_last_digest_date() -> str:
    """Get date of last digest run."""
    import sys
    sys.path.insert(0, str(LIB_PATH / "pipelines"))
    from digest import get_last_run_date
    return get_last_run_date()


def get_new_pages(since_date: str) -> list:
    """Get pages added since the given date."""
    manifest = load_manifest()
    if not manifest:
        return []

    since_dt = datetime.strptime(since_date, "%Y-%m-%d").date()
    all_pages = manifest.get("pages", [])
    new_pages = []
    for page in all_pages:
        extracted_at = page.get("extracted_at")
        if extracted_at:
            if isinstance(extracted_at, date):
                if extracted_at >= since_dt:
                    new_pages.append(page)
            elif str(extracted_at) >= since_date:
                new_pages.append(page)
    return new_pages


def get_agents() -> list:
    """Get all agents with their configurations."""
    agents = []

    if not AGENTS_PATH.exists():
        return agents

    for agent_dir in AGENTS_PATH.iterdir():
        if not agent_dir.is_dir():
            continue

        # Read identity.yaml
        identity_file = agent_dir / "identity.yaml"
        if not identity_file.exists():
            continue

        with open(identity_file) as f:
            content = f.read()
            # Try to extract YAML frontmatter, skip if parsing fails
            try:
                if content.startswith("---"):
                    # Find the closing ---
                    lines = content.split("\n")
                    frontmatter_lines = []
                    in_frontmatter = False
                    for i, line in enumerate(lines):
                        if i == 0 and line == "---":
                            in_frontmatter = True
                            continue
                        if in_frontmatter and line == "---":
                            break
                        frontmatter_lines.append(line)
                    frontmatter = "\n".join(frontmatter_lines)
                    identity = yaml.safe_load(frontmatter) or {}
                else:
                    identity = yaml.safe_load(content) or {}
            except Exception:
                # Skip agents with malformed YAML
                identity = {}

        # Look for watch_tags in inbox/config.json
        config_file = agent_dir / "inbox" / "config.json"
        watch_tags = []
        if config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
                watch_tags = config.get("watch_tags", [])

        # Fallback: infer from agent name
        if not watch_tags:
            agent_name = agent_dir.name.lower()
            # Map agent types to tags
            if "youtube" in agent_name:
                watch_tags = ["youtube", "video", "ai_research"]
            elif "twitter" in agent_name:
                watch_tags = ["twitter", "social", "discovery"]
            elif "reddit" in agent_name:
                watch_tags = ["reddit", "social", "discovery"]
            elif "github" in agent_name:
                watch_tags = ["github", "code", "engineering"]
            elif "web" in agent_name:
                watch_tags = ["web", "article", "discovery"]

        # Check for inbox directory
        inbox_dir = agent_dir / "inbox"
        has_inbox = inbox_dir.exists() and inbox_dir.is_dir()

        agents.append({
            "name": agent_dir.name,
            "id": identity.get("agent_id", f"library:{agent_dir.name}"),
            "watch_tags": watch_tags,
            "inbox_dir": str(inbox_dir) if has_inbox else None
        })

    return agents


def match_tags(page_tags: list, watch_tags: list) -> list:
    """Match page tags against watch tags."""
    page_tags_lower = set(t.lower() for t in page_tags)
    watch_tags_lower = set(t.lower() for t in watch_tags)

    # Direct match
    matched = page_tags_lower & watch_tags_lower
    if matched:
        return list(matched)

    # Check if any page tag contains watch tag or vice versa
    for pt in page_tags_lower:
        for wt in watch_tags_lower:
            if wt in pt or pt in wt:
                matched.add(wt)

    return list(matched)


def generate_notification(agent: dict, pages: list, date: str) -> dict:
    """Generate notification for an agent."""
    matched_pages = []

    for page in pages:
        page_tags = page.get("tags", [])
        # Infer tags from shelf if none provided
        if not page_tags:
            shelf = page.get("shelf", "")
            if shelf:
                topic = shelf.split("/")[-1] if "/" in shelf else shelf
                page_tags = [topic]

        matched = match_tags(page_tags, agent["watch_tags"])
        if matched:
            matched_pages.append({
                "id": page.get("id"),
                "title": page.get("title", "Untitled"),
                "shelf": page.get("shelf", ""),
                "tags": page_tags,
                "tier": page.get("tier", "B"),
                "creator": page.get("creator", ""),
                "matched_tags": matched
            })

    if not matched_pages:
        return None

    return {
        "type": "digest",
        "date": date,
        "agent_id": agent["id"],
        "agent_name": agent["name"],
        "pages": matched_pages,
        "matched_tags": list(set(tag for p in matched_pages for tag in p.get("matched_tags", []))),
        "generated_at": datetime.now(timezone.utc).isoformat() + "Z"
    }


def run_notify(dry_run: bool, date: str = None):
    """Run the notification pipeline."""
    # Get date of last digest
    import sys
    sys.path.insert(0, str(LIB_PATH / "pipelines"))
    from digest import get_last_run_date
    last_run = get_last_run_date()

    if date:
        target_date = date
    else:
        target_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print(f"Generating notifications for {target_date} (last digest: {last_run})")

    # Get new pages since last digest
    new_pages = get_new_pages(last_run)
    print(f"New pages since {last_run}: {len(new_pages)}")

    # Get all agents
    agents = get_agents()
    print(f"Found {len(agents)} agents")

    notifications_sent = 0

    for agent in agents:
        print(f"\nProcessing agent: {agent['name']}")
        print(f"  Watch tags: {agent['watch_tags']}")

        if not agent["watch_tags"]:
            print(f"  No watch tags configured, skipping")
            continue

        if not agent["inbox_dir"]:
            print(f"  No inbox directory, skipping")
            continue

        # Generate notification
        notification = generate_notification(agent, new_pages, target_date)

        if not notification:
            print(f"  No matching pages")
            continue

        print(f"  Matched {len(notification['pages'])} pages")

        if dry_run:
            print(f"  [DRY RUN] Would write notification to {agent['inbox_dir']}/digest_{target_date}.json")
            continue

        # Write notification
        inbox_path = Path(agent["inbox_dir"])
        inbox_path.mkdir(parents=True, exist_ok=True)

        notif_file = inbox_path / f"digest_{target_date}.json"
        with open(notif_file, "w") as f:
            json.dump(notification, f, indent=2)

        print(f"  Written: {notif_file}")
        notifications_sent += 1

    print(f"\nNotifications sent: {notifications_sent}")


def main():
    parser = argparse.ArgumentParser(description="Push relevant pages to subscribed agents")
    parser.add_argument("--date", type=str, default="",
                        help="Target date for notifications (YYYY-MM-DD), default: today")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be sent without writing")
    args = parser.parse_args()

    run_notify(args.dry_run, args.date)


if __name__ == "__main__":
    main()
