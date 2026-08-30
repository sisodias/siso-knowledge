#!/usr/bin/env python3
"""Validation tests for the people knowledge registry."""

import unittest
import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from registry import load_people, people_by_slug
from scorer import update_person_tier


class PeopleRegistryTest(unittest.TestCase):
    def test_registry_loads_core_people_and_historical_figures(self):
        people = load_people()
        by_slug = people_by_slug(people)

        required_slugs = {
            "jensen-huang",
            "dario-amodei",
            "sam-altman",
            "demis-hassabis",
            "tim-cook",
            "john-ternus",
            "brian-chesky",
            "brian-armstrong",
            "tobi-lutke",
            "lisa-su",
            "cc-wei",
            "safra-catz",
            "arvind-krishna",
            "socrates",
            "marcus-aurelius",
            "alex-hormozi",
            "bob-proctor",
        }

        self.assertGreaterEqual(len(people), 90)
        self.assertTrue(required_slugs.issubset(by_slug.keys()))

    def test_registry_has_unique_slugs_and_collection_modes(self):
        people = load_people()
        slugs = [person["slug"] for person in people]

        self.assertEqual(len(slugs), len(set(slugs)))
        for person in people:
            self.assertIn(person["status"], {"approved", "candidate", "maybe", "rejected"})
            self.assertIn(
                person["collection_mode"],
                {"direct-source-first", "social-first", "corpus-first", "manual-curation"},
            )
            self.assertIsInstance(person.get("topics", []), list)
            self.assertIsInstance(person.get("sources", []), list)

    def test_scorer_preserves_curated_tier_without_metrics(self):
        person = {
            "name": "Marcus Aurelius",
            "slug": "marcus-aurelius",
            "handle": "",
            "tier": "S",
            "follower_count": 0,
        }

        with contextlib.redirect_stdout(io.StringIO()):
            updated = update_person_tier(person, dry_run=True)

        self.assertEqual(updated["tier"], "S")


if __name__ == "__main__":
    unittest.main()
