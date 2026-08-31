#!/usr/bin/env python3
"""Tests for person dossier generation."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parents[1] / "youtube"))

from acquisition import PeopleVideoQueue  # noqa: E402
from dossier_builder import build_dossier, write_dossiers  # noqa: E402


class PeopleDossierBuilderTest(unittest.TestCase):
    def test_build_dossier_includes_registry_fields_and_video_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = PeopleVideoQueue(Path(tmp) / "queue.sqlite")
            person = {
                "name": "Bob Lazar",
                "slug": "bob-lazar",
                "status": "maybe",
                "line": "manual-review-interview-subjects",
                "role": "Interview subject and controversial aerospace claimant",
                "tier": "C",
                "collection_mode": "manual-curation",
                "topics": ["interviews", "ufology"],
                "sources": [],
                "notes": "Treat as source material, not verified factual authority.",
                "weight": 1.0,
            }
            queue.add_manual_video(
                person,
                "https://www.youtube.com/watch?v=BEWz4SXfyCQ",
                title="Joe Rogan Experience #1315 - Bob Lazar & Jeremy Corbell",
                channel_name="PowerfulJRE",
            )

            dossier = build_dossier(person, queue)
            self.assertEqual(dossier["slug"], "bob-lazar")
            self.assertEqual(dossier["video_counts"]["candidate"], 1)
            self.assertEqual(dossier["video_counts"]["transcript_ready"], 0)
            self.assertIn("BEWz4SXfyCQ", dossier["videos"][0]["url"])
            self.assertIn("bob-lazar__BEWz4SXfyCQ__", dossier["videos"][0]["suggested_transcript_filename"])
            self.assertEqual(dossier["next_action"], "import_transcript")
            self.assertEqual(dossier["source_plan"]["next_source_action"], "manual_review")

    def test_write_dossiers_creates_index_json_and_markdown_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            queue = PeopleVideoQueue(tmp_path / "queue.sqlite")
            person = {
                "name": "Dario Amodei",
                "slug": "dario-amodei",
                "status": "approved",
                "line": "frontier-ai-company-leaders",
                "role": "Co-founder and CEO, Anthropic",
                "tier": "S",
                "collection_mode": "direct-source-first",
                "topics": ["ai safety", "frontier models"],
                "sources": [{"type": "official", "url": "https://www.anthropic.com"}],
                "notes": "",
                "weight": 4.0,
            }
            output_dir = tmp_path / "dossiers"

            summary = write_dossiers([person], queue, output_dir)
            self.assertEqual(summary["people_count"], 1)
            self.assertTrue((output_dir / "dario-amodei.md").exists())
            self.assertTrue((output_dir / "index.json").exists())
            self.assertIn("Dario Amodei", (output_dir / "dario-amodei.md").read_text())
            self.assertEqual(json.loads((output_dir / "index.json").read_text())["people"][0]["slug"], "dario-amodei")

    def test_corpus_first_dossier_uses_source_plan_not_youtube_queries(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = PeopleVideoQueue(Path(tmp) / "queue.sqlite")
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
                "notes": "",
                "weight": 4.0,
            }

            dossier = build_dossier(person, queue)

            self.assertEqual(dossier["next_action"], "collect_corpus_sources")
            self.assertEqual(dossier["search_queries"], [])
            self.assertTrue(any("gutenberg.org" in target["url"] for target in dossier["source_plan"]["source_targets"]))
            self.assertIn("Socrates left no writings", dossier["source_plan"]["curation_notes"][0])


if __name__ == "__main__":
    unittest.main()
