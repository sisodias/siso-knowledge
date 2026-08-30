#!/usr/bin/env python3
"""Tests for safe raw source ingestion from source plans."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from source_ingest import build_gutenberg_text_url, collect_public_domain_sources  # noqa: E402


class PeopleSourceIngestTest(unittest.TestCase):
    def test_build_gutenberg_text_url_from_ebook_page(self):
        self.assertEqual(
            build_gutenberg_text_url("https://www.gutenberg.org/ebooks/2680"),
            "https://www.gutenberg.org/ebooks/2680.txt.utf-8",
        )
        self.assertEqual(build_gutenberg_text_url("https://example.com/nope"), "")

    def test_collect_public_domain_sources_writes_raw_files_and_manifest(self):
        def fake_fetch(url: str) -> str:
            return f"Downloaded from {url}\n\nText body"

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
                "name": "Dario Amodei",
                "slug": "dario-amodei",
                "status": "approved",
                "line": "frontier-ai-company-leaders",
                "role": "Co-founder and CEO, Anthropic",
                "tier": "S",
                "collection_mode": "direct-source-first",
                "topics": ["ai safety"],
                "sources": [{"type": "official", "url": "https://www.anthropic.com"}],
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            manifest = collect_public_domain_sources(people, Path(tmp), fetcher=fake_fetch)

            self.assertEqual(manifest["sources_count"], 1)
            item = manifest["sources"][0]
            self.assertEqual(item["person_slug"], "marcus-aurelius")
            self.assertEqual(item["repository"], "Project Gutenberg")
            self.assertEqual(item["rights_status"], "public_domain_source")
            self.assertTrue(Path(item["local_path"]).exists())
            self.assertIn("source_url", item)
            self.assertEqual(json.loads((Path(tmp) / "manifest.json").read_text())["sources_count"], 1)


if __name__ == "__main__":
    unittest.main()
