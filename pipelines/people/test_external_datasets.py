#!/usr/bin/env python3
"""Smoke tests for the external people dataset registry."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))

from external_dataset_reporter import render_status  # noqa: E402


class ExternalDatasetsTest(unittest.TestCase):
    def test_registry_has_required_fields_and_core_hits(self):
        path = Path(__file__).with_name("external_datasets.yaml")
        data = yaml.safe_load(path.read_text())
        self.assertIn("datasets", data)

        ids = {dataset["id"] for dataset in data["datasets"]}
        self.assertIn("scribesalad", ids)
        self.assertIn("hormozi-wiki", ids)
        self.assertIn("lex-fridman-hf-nmac", ids)
        self.assertIn("lex-fridman-hf-aditya0619", ids)
        self.assertIn("lenny-podcast-transcripts-chatprd", ids)
        self.assertIn("wikidata-official-dumps", ids)
        self.assertIn("quotekg", ids)
        self.assertIn("youtube-commons-pleias", ids)

        for dataset in data["datasets"]:
            with self.subTest(dataset=dataset["id"]):
                self.assertTrue(dataset["name"])
                self.assertTrue(dataset["url"].startswith("https://"))
                self.assertIn(dataset["status"], data["dataset_statuses"])
                self.assertIsInstance(dataset.get("mapped_people", []), list)
                self.assertTrue(dataset.get("import_strategy"))
                self.assertIn("observed_at", dataset)
                self.assertIn("source_last_updated", dataset)
                self.assertIn("freshness_notes", dataset)

    def test_status_report_surfaces_p0_candidates_and_gaps(self):
        path = Path(__file__).with_name("external_datasets.yaml")
        data = yaml.safe_load(path.read_text())
        report = render_status(data)
        self.assertIn("ScribeSalad", report)
        self.assertIn("Wikidata official dumps", report)
        self.assertIn("P0 Import Candidates", report)
        self.assertIn("Source last updated", report)
        self.assertIn("Data coverage", report)
        self.assertIn("Data volume", report)
        self.assertIn("Data Volume Inventory", report)
        self.assertIn("bob-proctor-public-corpus-gap", report)


if __name__ == "__main__":
    unittest.main()
