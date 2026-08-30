#!/usr/bin/env python3
"""Tests for non-YouTube source planning by person."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from source_planner import build_source_plan, write_source_plans  # noqa: E402


class PeopleSourcePlannerTest(unittest.TestCase):
    def test_corpus_first_historical_plan_prefers_primary_text_archives(self):
        person = {
            "name": "Socrates",
            "slug": "socrates",
            "status": "approved",
            "line": "historic-philosophy-fundamental-thinkers",
            "role": "Classical Greek philosopher",
            "tier": "S",
            "collection_mode": "corpus-first",
            "topics": ["questioning", "ethics"],
            "sources": [],
        }

        plan = build_source_plan(person)

        self.assertEqual(plan["source_strategy"], "corpus")
        self.assertEqual(plan["next_source_action"], "collect_corpus_sources")
        self.assertFalse(any("youtube.com" in target["url"] for target in plan["source_targets"]))
        self.assertTrue(any("gutenberg.org" in target["url"] for target in plan["source_targets"]))
        self.assertTrue(any("perseus.tufts.edu" in target["url"] for target in plan["source_targets"]))
        self.assertIn("Socrates left no writings", plan["curation_notes"][0])

    def test_direct_source_plan_keeps_registry_sources_and_discovery_urls(self):
        person = {
            "name": "Dario Amodei",
            "slug": "dario-amodei",
            "status": "approved",
            "line": "frontier-ai-company-leaders",
            "role": "Co-founder and CEO, Anthropic",
            "tier": "S",
            "collection_mode": "direct-source-first",
            "topics": ["ai safety"],
            "sources": [{"type": "official", "url": "https://www.anthropic.com"}],
        }

        plan = build_source_plan(person)

        self.assertEqual(plan["source_strategy"], "direct")
        self.assertEqual(plan["next_source_action"], "collect_direct_sources")
        self.assertEqual(plan["source_targets"][0]["url"], "https://www.anthropic.com")
        self.assertTrue(any("youtube.com/results" in url for url in plan["discovery_urls"]))

    def test_elon_musk_plan_is_full_lifecycle_not_just_social(self):
        person = {
            "name": "Elon Musk",
            "slug": "elon-musk",
            "status": "approved",
            "line": "frontier-ai-company-leaders",
            "role": "CEO, xAI / Tesla / SpaceX",
            "tier": "S",
            "collection_mode": "social-first",
            "topics": ["agi", "autonomous vehicles", "robotics"],
            "sources": [
                {"type": "x", "url": "https://x.com/elonmusk"},
                {"type": "official", "url": "https://www.tesla.com/elon-musk"},
            ],
        }

        plan = build_source_plan(person)
        target_urls = {target["url"] for target in plan["source_targets"]}
        target_types = {target["type"] for target in plan["source_targets"]}

        self.assertEqual(plan["source_strategy"], "social")
        self.assertEqual(plan["next_source_action"], "collect_social_and_longform_sources")
        self.assertGreaterEqual(plan["source_counts"]["targets"], 18)
        self.assertIn("https://www.everyelonmuskinterview.com/", target_urls)
        self.assertIn("https://ir.tesla.com/#events-and-presentations", target_urls)
        self.assertIn("https://www.sec.gov/edgar/browse/?CIK=1318605", target_urls)
        self.assertIn("official_podcast_transcripts", target_types)
        self.assertIn("podcast_appearance_discovery", target_types)
        self.assertTrue(any("Joe+Rogan" in url for url in plan["discovery_urls"]))

    def test_rights_review_is_explicit_for_modern_corpus_people(self):
        person = {
            "name": "Carl Jung",
            "slug": "carl-jung",
            "status": "candidate",
            "line": "historic-philosophy-fundamental-thinkers",
            "role": "Psychiatrist and psychoanalyst",
            "tier": "A",
            "collection_mode": "corpus-first",
            "topics": ["archetypes"],
            "sources": [],
        }

        plan = build_source_plan(person)

        self.assertEqual(plan["next_source_action"], "rights_review_before_ingest")
        self.assertTrue(any(target["rights_status"] == "rights_review" for target in plan["source_targets"]))

    def test_write_source_plans_creates_index_and_backlog(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "source_plans"
            people = [
                {
                    "name": "Marcus Aurelius",
                    "slug": "marcus-aurelius",
                    "status": "approved",
                    "line": "historic-philosophy-fundamental-thinkers",
                    "role": "Roman emperor and Stoic philosopher",
                    "tier": "S",
                    "collection_mode": "corpus-first",
                    "topics": ["stoicism"],
                    "sources": [],
                },
                {
                    "name": "Bob Lazar",
                    "slug": "bob-lazar",
                    "status": "maybe",
                    "line": "manual-review-interview-subjects",
                    "role": "Interview subject",
                    "tier": "C",
                    "collection_mode": "manual-curation",
                    "topics": ["interviews"],
                    "sources": [],
                },
            ]

            index = write_source_plans(people, output_dir)

            self.assertEqual(index["people_count"], 2)
            self.assertEqual(index["totals"]["collect_corpus_sources"], 1)
            self.assertEqual(index["totals"]["manual_review"], 1)
            self.assertTrue((output_dir / "marcus-aurelius.json").exists())
            self.assertTrue((output_dir / "source_backlog.md").exists())
            self.assertIn("Marcus Aurelius", (output_dir / "source_backlog.md").read_text())
            self.assertEqual(json.loads((output_dir / "index.json").read_text())["people"][0]["slug"], "marcus-aurelius")


if __name__ == "__main__":
    unittest.main()
