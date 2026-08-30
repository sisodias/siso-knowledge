#!/usr/bin/env python3
"""Build source acquisition plans for people beyond YouTube video discovery."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
sys.path.insert(0, str(ROOT / "pipelines" / "people"))

from registry import load_people  # noqa: E402

DEFAULT_SOURCE_PLAN_DIR = ROOT / "pipelines" / "people" / "source_plans"

MODERN_CORPUS_RIGHTS_REVIEW = {
    "aldous-huxley",
    "bob-proctor",
    "carl-jung",
    "carl-sagan",
    "daniel-kahneman",
    "earl-nightingale",
    "george-orwell",
    "henry-kissinger",
    "isaac-asimov",
    "jim-rohn",
    "joseph-campbell",
    "lee-kuan-yew",
    "marshall-mcluhan",
    "martin-luther-king-jr",
    "nelson-mandela",
    "peter-drucker",
    "rene-girard",
    "richard-feynman",
    "viktor-frankl",
    "w-edwards-deming",
    "winston-churchill",
}

CURATED_SOURCE_TARGETS: dict[str, list[dict[str, str]]] = {
    "socrates": [
        {
            "title": "Apology, Crito, and Phaedo of Socrates",
            "repository": "Project Gutenberg",
            "type": "canonical_text",
            "url": "https://www.gutenberg.org/ebooks/13726",
            "rights_status": "public_domain_source",
            "notes": "Plato dialogues centered on Socrates; use as attributed Plato source material.",
        },
        {
            "title": "Plato, Apology",
            "repository": "Perseus Digital Library",
            "type": "classical_text",
            "url": "https://www.perseus.tufts.edu/hopper/collection?collection=Perseus%3Acorpus%3Aperseus%2Cwork%2CPlato%2C+Apology",
            "rights_status": "public_domain_source",
            "notes": "Primary classical text access; prefer structured citation by dialogue/section.",
        },
    ],
    "plato": [
        {
            "title": "Books by Plato",
            "repository": "Project Gutenberg",
            "type": "author_collection",
            "url": "https://www.gutenberg.org/ebooks/author/93",
            "rights_status": "public_domain_source",
            "notes": "Download individual dialogue texts rather than scraping search pages.",
        },
        {
            "title": "Plato corpus search",
            "repository": "Perseus Digital Library",
            "type": "classical_text_search",
            "url": "https://www.perseus.tufts.edu/hopper/searchresults?q=Plato",
            "rights_status": "public_domain_source",
            "notes": "Use for Greek/English text references and stable passage identifiers.",
        },
    ],
    "marcus-aurelius": [
        {
            "title": "Meditations",
            "repository": "Project Gutenberg",
            "type": "canonical_text",
            "url": "https://www.gutenberg.org/ebooks/2680",
            "rights_status": "public_domain_source",
            "notes": "Public-domain translation suitable for full-text ingestion.",
        },
        {
            "title": "Meditations translation index",
            "repository": "Wikisource",
            "type": "translation_index",
            "url": "https://en.wikisource.org/wiki/Meditations",
            "rights_status": "translation_rights_review",
            "notes": "Pick a public-domain translation before ingestion; preserve translator metadata.",
        },
    ],
    "epictetus": [
        {
            "title": "The Enchiridion",
            "repository": "Project Gutenberg",
            "type": "canonical_text",
            "url": "https://www.gutenberg.org/ebooks/45109",
            "rights_status": "public_domain_source",
            "notes": "Public-domain English translation; store Arrian/compiler and translator metadata.",
        },
        {
            "title": "A Selection from the Discourses of Epictetus with the Encheiridion",
            "repository": "Project Gutenberg",
            "type": "canonical_text",
            "url": "https://www.gutenberg.org/ebooks/10661",
            "rights_status": "public_domain_source",
            "notes": "Public-domain selection; preserve edition and translator metadata.",
        },
        {
            "title": "Books by Epictetus",
            "repository": "Project Gutenberg",
            "type": "author_collection",
            "url": "https://www.gutenberg.org/ebooks/author/452",
            "rights_status": "public_domain_source",
            "notes": "Includes Enchiridion and Discourses material in public-domain editions.",
        },
        {
            "title": "The Encheiridion or Manual",
            "repository": "Wikisource",
            "type": "canonical_text",
            "url": "https://en.wikisource.org/wiki/The_Discourses_of_Epictetus%3B_with_the_Encheiridion_and_Fragments/The_Encheiridion_or_Manual",
            "rights_status": "public_domain_source",
            "notes": "Epictetus was transmitted by Arrian; store attribution clearly.",
        },
    ],
    "adam-smith": [
        {
            "title": "An Inquiry into the Nature and Causes of the Wealth of Nations",
            "repository": "Project Gutenberg",
            "type": "canonical_text",
            "url": "https://www.gutenberg.org/ebooks/3300",
            "rights_status": "public_domain_source",
            "notes": "Core economics text; segment by book/chapter.",
        },
    ],
    "benjamin-franklin": [
        {
            "title": "Autobiography of Benjamin Franklin",
            "repository": "Project Gutenberg",
            "type": "canonical_text",
            "url": "https://www.gutenberg.org/ebooks/20203",
            "rights_status": "public_domain_source",
            "notes": "Public-domain edition; distinguish Franklin-authored text from editor/illustrator metadata.",
        },
        {
            "title": "Books by Benjamin Franklin",
            "repository": "Project Gutenberg",
            "type": "author_collection",
            "url": "https://www.gutenberg.org/ebooks/author/92",
            "rights_status": "public_domain_source",
            "notes": "Prefer Autobiography plus selected letters/essays with edition metadata.",
        },
        {
            "title": "Benjamin Franklin resources",
            "repository": "Library of Congress",
            "type": "archive_guide",
            "url": "https://www.loc.gov/rr/program/bib/franklin/",
            "rights_status": "rights_review",
            "notes": "Use as discovery guide; verify item-level rights before full-text ingestion.",
        },
    ],
    "frederick-douglass": [
        {
            "title": "Narrative of the Life of Frederick Douglass",
            "repository": "Project Gutenberg",
            "type": "canonical_text",
            "url": "https://www.gutenberg.org/ebooks/23",
            "rights_status": "public_domain_source",
            "notes": "Public-domain autobiography; segment by chapter and preserve edition info.",
        },
    ],
    "elon-musk": [
        {
            "title": "Every Elon Musk Interview year index",
            "repository": "Every Elon Musk Interview",
            "type": "lifetime_interview_index",
            "url": "https://www.everyelonmuskinterview.com/",
            "rights_status": "discovery_only_rights_review",
            "notes": "Use as the spine for lifetime interview discovery across years; store event date, host, venue, media URL, transcript availability, and original source URL.",
        },
        {
            "title": "Elon Musk Interviews transcript archive",
            "repository": "Elon Musk Interviews",
            "type": "fan_transcript_archive",
            "url": "https://elon-musk-interviews.com/",
            "rights_status": "rights_review",
            "notes": "Contains segmented English/German transcripts for major interviews such as Joe Rogan and TED; treat as secondary unless original transcript/source is verified.",
        },
        {
            "title": "Lex Fridman Elon Musk transcript pages",
            "repository": "Lex Fridman",
            "type": "official_podcast_transcripts",
            "url": "https://lexfridman.com/?s=Elon+Musk+transcript",
            "rights_status": "rights_review",
            "notes": "Official Lex transcript pages/PDFs cover multiple longform Elon interviews; preserve episode number, date, timestamps, and transcript page URL.",
        },
        {
            "title": "TED Elon Musk speaker page",
            "repository": "TED",
            "type": "official_talk_index",
            "url": "https://www.ted.com/speakers/elon_musk",
            "rights_status": "rights_review",
            "notes": "Official TED index for 2013, 2017, and 2022 Elon talks/interviews; use talk pages as primary metadata and transcript/caption sources where permitted.",
        },
        {
            "title": "The Henry Ford OnInnovation Elon Musk oral history",
            "repository": "The Henry Ford",
            "type": "official_oral_history_transcript",
            "url": "https://www.thehenryford.org/docs/thehenryfordlibraries/innovator-transcripts/transcript_musk_full-length5a30f6547bde445e8119d53fb454b300.pdf",
            "rights_status": "rights_review",
            "notes": "Full-length 2008 oral-history interview transcript; high-priority early-career primary-ish source.",
        },
        {
            "title": "Tesla Investor Relations events and presentations",
            "repository": "Tesla Investor Relations",
            "type": "official_company_event_index",
            "url": "https://ir.tesla.com/#events-and-presentations",
            "rights_status": "rights_review",
            "notes": "Official source for earnings calls, shareholder meetings, AI Day, Autonomy Day, Battery Day, product/event presentations, and webcast metadata.",
        },
        {
            "title": "Tesla SEC EDGAR company filings",
            "repository": "SEC EDGAR",
            "type": "regulatory_filings",
            "url": "https://www.sec.gov/edgar/browse/?CIK=1318605",
            "rights_status": "public_regulatory_records",
            "notes": "Use for letters, exhibits, proxy statements, 10-K/10-Q/8-K, and quoted executive statements; connect to Musk only when speaker/author is explicit.",
        },
        {
            "title": "Tesla press releases and company blog",
            "repository": "Tesla",
            "type": "official_company_archive",
            "url": "https://www.tesla.com/blog",
            "rights_status": "rights_review",
            "notes": "Official company posts and announcements; identify Musk-authored or Musk-quoted items separately from generic company copy.",
        },
        {
            "title": "SpaceX news and updates",
            "repository": "SpaceX",
            "type": "official_company_archive",
            "url": "https://www.spacex.com/updates/",
            "rights_status": "rights_review",
            "notes": "Official SpaceX update archive; useful for launch talks, Starship updates, and Musk-quoted company material.",
        },
        {
            "title": "xAI news and blog",
            "repository": "xAI",
            "type": "official_company_archive",
            "url": "https://x.ai/news",
            "rights_status": "rights_review",
            "notes": "Official xAI announcements and Grok-related material; connect to Musk only where authored, quoted, or primary-source-linked.",
        },
        {
            "title": "Neuralink blog",
            "repository": "Neuralink",
            "type": "official_company_archive",
            "url": "https://neuralink.com/blog/",
            "rights_status": "rights_review",
            "notes": "Official Neuralink updates; cross-link with Musk talks/interviews about brain-computer interfaces.",
        },
        {
            "title": "X account and social archive",
            "repository": "X",
            "type": "social_archive",
            "url": "https://x.com/elonmusk",
            "rights_status": "api_or_user_export_required",
            "notes": "Do not scrape logged-in X pages blindly. Prefer user export, official API, archived public URLs, or licensed datasets; preserve post ID, timestamp, reply/quote context, and deletion status.",
        },
        {
            "title": "Podchaser Elon Musk podcast appearances",
            "repository": "Podchaser API",
            "type": "podcast_appearance_discovery",
            "url": "https://www.podchaser.com/api",
            "rights_status": "api_terms",
            "notes": "Use person/credit search to discover podcast appearances and transcript availability across millions of episodes.",
        },
        {
            "title": "Podscan Elon Musk transcript/entity search",
            "repository": "Podscan API",
            "type": "podcast_transcript_search",
            "url": "https://help.podscan.fm/en/article/building-podcast-powered-applications-with-the-podscan-api-13741kz/",
            "rights_status": "api_terms",
            "notes": "Use for rolling monitoring of new Elon mentions/appearances and transcript availability; entity matches require verification.",
        },
        {
            "title": "spoken.md targeted transcript fetch",
            "repository": "spoken.md",
            "type": "on_demand_transcript_fetch",
            "url": "https://spoken.md/",
            "rights_status": "commercial_api_terms",
            "notes": "Use after the interview index identifies high-priority podcast episodes needing transcripts.",
        },
        {
            "title": "Kurry S&P 500 earnings transcripts",
            "repository": "Hugging Face",
            "type": "earnings_call_dataset",
            "url": "https://huggingface.co/datasets/kurry/sp500_earnings_transcripts",
            "rights_status": "rights_review",
            "notes": "Use to backfill Tesla earnings-call transcript rows from 2005-2025 and map speaker/date/company edges.",
        },
        {
            "title": "YouTube Commons CC-BY transcript corpus",
            "repository": "Hugging Face",
            "type": "cc_by_youtube_transcript_search",
            "url": "https://huggingface.co/datasets/PleIAs/YouTube-Commons",
            "rights_status": "cc-by-4.0_with_attribution",
            "notes": "Filter CC-BY YouTube transcripts by Elon/Tesla/SpaceX/xAI titles and channels for rights-clean backfill.",
        },
        {
            "title": "Internet Archive Elon Musk media search",
            "repository": "Internet Archive",
            "type": "media_archive_search",
            "url": "https://archive.org/search?query=%22Elon+Musk%22",
            "rights_status": "item_level_rights_review",
            "notes": "Use for older talks, TV appearances, event recordings, and archived web/media items; rights vary per item.",
        },
        {
            "title": "CourtListener Elon Musk search",
            "repository": "CourtListener",
            "type": "legal_records_search",
            "url": "https://www.courtlistener.com/?q=%22Elon%20Musk%22",
            "rights_status": "public_records_with_item_terms",
            "notes": "Use for depositions, exhibits, opinions, and filings containing Musk statements; distinguish quoted speech from lawyer narration.",
        },
        {
            "title": "Google Patents Elon Musk inventor search",
            "repository": "Google Patents",
            "type": "patent_records_search",
            "url": "https://patents.google.com/?inventor=Elon+Musk",
            "rights_status": "public_patent_records",
            "notes": "Use for early technical/inventor records; likely metadata-first, not worldview text.",
        },
    ],
    "george-orwell": [
        {
            "title": "Essays and other works",
            "repository": "The Orwell Foundation",
            "type": "official_archive",
            "url": "https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/",
            "rights_status": "rights_review",
            "notes": "Use as a discovery and citation guide; do not bulk-ingest without rights review.",
        },
    ],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def discovery_url(repository: str, query: str) -> str:
    encoded = quote_plus(query)
    if repository == "Project Gutenberg":
        return f"https://www.gutenberg.org/ebooks/search/?query={encoded}"
    if repository == "Wikisource":
        return f"https://en.wikisource.org/w/index.php?search={encoded}"
    if repository == "Internet Archive":
        return f"https://archive.org/search?query={encoded}"
    if repository == "Open Library":
        return f"https://openlibrary.org/search?q={encoded}"
    if repository == "YouTube":
        return f"https://www.youtube.com/results?search_query={encoded}"
    if repository == "Web":
        return f"https://www.google.com/search?q={encoded}"
    raise ValueError(f"Unknown repository: {repository}")


def registry_source_targets(person: dict[str, Any]) -> list[dict[str, str]]:
    targets = []
    for source in person.get("sources", []):
        url = source.get("url", "")
        if not url:
            continue
        source_type = source.get("type", "source")
        targets.append(
            {
                "title": f"{person['name']} {source_type}",
                "repository": source_type,
                "type": "registry_source",
                "url": url,
                "rights_status": "rights_review",
                "notes": "Registry-provided source; verify page-specific reuse rights before bulk ingestion.",
            }
        )
    return targets


def generic_corpus_targets(person: dict[str, Any], rights_status: str) -> list[dict[str, str]]:
    query = person["name"]
    repositories = ["Project Gutenberg", "Wikisource", "Internet Archive", "Open Library"]
    if any(token in person.get("role", "").lower() for token in ["greek", "roman", "classical"]):
        repositories.append("Perseus")

    targets = []
    for repository in repositories:
        if repository == "Perseus":
            url = f"https://www.perseus.tufts.edu/hopper/searchresults?q={quote_plus(query)}"
        else:
            url = discovery_url(repository, query)
        targets.append(
            {
                "title": f"{query} source search",
                "repository": repository,
                "type": "archive_search",
                "url": url,
                "rights_status": rights_status,
                "notes": "Discovery target; select item-level texts and preserve edition/translator metadata.",
            }
        )
    return targets


def direct_discovery_urls(person: dict[str, Any]) -> list[str]:
    name = person["name"]
    topics = [topic for topic in person.get("topics", []) if isinstance(topic, str)]
    queries = [
        f'"{name}" official essays interviews',
        f'"{name}" site:youtube.com interview',
        f'"{name}" site:youtube.com keynote',
    ]
    for topic in topics[:2]:
        queries.append(f'"{name}" {topic}')
    return [discovery_url("YouTube" if "youtube" in query else "Web", query) for query in queries]


def elon_musk_discovery_urls() -> list[str]:
    queries = [
        '"Elon Musk" interview transcript',
        '"Elon Musk" podcast transcript',
        '"Elon Musk" "Joe Rogan" transcript',
        '"Elon Musk" "Lex Fridman" transcript',
        '"Elon Musk" TED transcript',
        '"Elon Musk" "Code Conference" transcript',
        '"Elon Musk" "SXSW" transcript',
        '"Elon Musk" "World Government Summit" transcript',
        '"Elon Musk" "Tesla earnings call" transcript',
        '"Elon Musk" "AI Day" transcript',
        '"Elon Musk" "Autonomy Day" transcript',
        '"Elon Musk" "Starship" presentation transcript',
        '"Elon Musk" "Neuralink" presentation transcript',
        '"Elon Musk" site:youtube.com interview',
        '"Elon Musk" site:youtube.com keynote',
    ]
    return [discovery_url("YouTube" if "youtube" in query else "Web", query) for query in queries]


def corpus_rights_status(person: dict[str, Any]) -> str:
    if person.get("slug") in MODERN_CORPUS_RIGHTS_REVIEW:
        return "rights_review"
    return "public_domain_or_translation_review"


def build_source_plan(person: dict[str, Any], target_limit: int = 8) -> dict[str, Any]:
    mode = person.get("collection_mode", "manual-curation")
    slug = person["slug"]
    curation_notes: list[str] = []

    if mode == "corpus-first":
        strategy = "corpus"
        rights_status = corpus_rights_status(person)
        targets = registry_source_targets(person)
        targets.extend(CURATED_SOURCE_TARGETS.get(slug, []))
        targets.extend(generic_corpus_targets(person, rights_status))
        if slug == "socrates":
            curation_notes.append(
                "Socrates left no writings; collect Plato, Xenophon, and Aristophanes material as attributed witness sources."
            )
        if rights_status == "rights_review":
            curation_notes.append(
                "Modern corpus entry: use official archives, public-domain items, or user-supplied material only after rights review."
            )
        next_action = "rights_review_before_ingest" if rights_status == "rights_review" else "collect_corpus_sources"
        discovery_urls = [target["url"] for target in targets if target["type"] == "archive_search"]
    elif mode == "direct-source-first":
        strategy = "direct"
        targets = registry_source_targets(person)
        next_action = "collect_direct_sources"
        discovery_urls = direct_discovery_urls(person)
    elif mode == "social-first":
        strategy = "social"
        targets = registry_source_targets(person)
        targets.extend(CURATED_SOURCE_TARGETS.get(slug, []))
        next_action = "collect_social_and_longform_sources"
        discovery_urls = elon_musk_discovery_urls() if slug == "elon-musk" else direct_discovery_urls(person)
    else:
        strategy = "manual"
        targets = registry_source_targets(person)
        targets.append(
            {
                "title": f"{person['name']} manual evidence file",
                "repository": "manual",
                "type": "manual_review",
                "url": "",
                "rights_status": "manual_review",
                "notes": "Curate claims, interviews, transcripts, and counter-sources before extraction.",
            }
        )
        next_action = "manual_review"
        discovery_urls = direct_discovery_urls(person)

    if slug == "elon-musk":
        target_limit = max(target_limit, 24)

    limited_targets = targets[:target_limit]
    return {
        "generated_at": utc_now(),
        "name": person["name"],
        "slug": slug,
        "status": person.get("status", "candidate"),
        "tier": person.get("tier", "B"),
        "line": person.get("line", ""),
        "role": person.get("role", ""),
        "collection_mode": mode,
        "source_strategy": strategy,
        "next_source_action": next_action,
        "topics": person.get("topics", []),
        "source_counts": {
            "targets": len(limited_targets),
            "discovery_urls": len(discovery_urls),
        },
        "source_targets": limited_targets,
        "discovery_urls": discovery_urls,
        "curation_notes": curation_notes,
    }


def render_plan_markdown(plan: dict[str, Any]) -> str:
    lines = [
        f"# {plan['name']} Source Plan",
        "",
        f"- Slug: `{plan['slug']}`",
        f"- Status: `{plan['status']}`",
        f"- Tier: `{plan['tier']}`",
        f"- Collection mode: `{plan['collection_mode']}`",
        f"- Source strategy: `{plan['source_strategy']}`",
        f"- Next source action: `{plan['next_source_action']}`",
        "",
        "## Source Targets",
        "",
    ]
    for target in plan["source_targets"]:
        label = f"{target['repository']} / {target['type']}"
        lines.append(f"- `{label}` {target['title']}")
        if target["url"]:
            lines.append(f"  - URL: {target['url']}")
        lines.append(f"  - Rights: `{target['rights_status']}`")
        if target.get("notes"):
            lines.append(f"  - Notes: {target['notes']}")

    if plan["discovery_urls"]:
        lines.extend(["", "## Discovery URLs", ""])
        lines.extend(f"- {url}" for url in plan["discovery_urls"])

    if plan["curation_notes"]:
        lines.extend(["", "## Curation Notes", ""])
        lines.extend(f"- {note}" for note in plan["curation_notes"])

    return "\n".join(lines).rstrip() + "\n"


def render_backlog_markdown(index: dict[str, Any]) -> str:
    lines = [
        "# People Source Backlog",
        "",
        f"Generated: `{index['generated_at']}`",
        f"People: `{index['people_count']}`",
        "",
        "## Totals",
        "",
    ]
    for action, count in sorted(index["totals"].items()):
        lines.append(f"- `{action}`: `{count}`")

    lines.extend(["", "## People", ""])
    for person in index["people"]:
        lines.append(
            f"- [{person['name']}]({Path(person['markdown_path']).name})"
            f" - `{person['next_source_action']}`"
            f" - targets `{person['source_counts']['targets']}`"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_source_plans(people: list[dict[str, Any]], output_dir: Path = DEFAULT_SOURCE_PLAN_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    plans = [build_source_plan(person) for person in people]

    for plan in plans:
        (output_dir / f"{plan['slug']}.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        (output_dir / f"{plan['slug']}.md").write_text(render_plan_markdown(plan), encoding="utf-8")

    totals: dict[str, int] = {}
    for plan in plans:
        action = plan["next_source_action"]
        totals[action] = totals.get(action, 0) + 1

    index = {
        "generated_at": utc_now(),
        "people_count": len(plans),
        "totals": totals,
        "people": [
            {
                "slug": plan["slug"],
                "name": plan["name"],
                "status": plan["status"],
                "tier": plan["tier"],
                "line": plan["line"],
                "collection_mode": plan["collection_mode"],
                "source_strategy": plan["source_strategy"],
                "next_source_action": plan["next_source_action"],
                "source_counts": plan["source_counts"],
                "markdown_path": str(output_dir / f"{plan['slug']}.md"),
                "json_path": str(output_dir / f"{plan['slug']}.json"),
            }
            for plan in plans
        ],
    }
    (output_dir / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    (output_dir / "source_backlog.md").write_text(render_backlog_markdown(index), encoding="utf-8")
    return index


def main() -> None:
    index = write_source_plans(load_people(), DEFAULT_SOURCE_PLAN_DIR)
    print(f"Wrote {index['people_count']} source plans to {DEFAULT_SOURCE_PLAN_DIR}")


if __name__ == "__main__":
    main()
