#!/usr/bin/env python3
"""Tests for people-centered YouTube acquisition helpers."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parents[1] / "people"))

from acquisition import (  # noqa: E402
    PeopleVideoQueue,
    build_person_queries,
    candidate_from_existing_record,
    extract_youtube_urls_from_text,
    extract_video_id,
    infer_person_slug_from_search_file,
    import_plugin_export_files,
    import_search_result_files,
    import_search_results,
    import_plugin_transcript,
    next_collection_action,
    parse_plugin_export_filename,
    record_matches_person,
    source_quality_adjustment,
    write_transcript_backlog,
    write_collection_report,
    write_query_plan,
)
from registry import load_people, people_by_slug  # noqa: E402


class YouTubeAcquisitionTest(unittest.TestCase):
    def test_extract_video_id_supports_common_youtube_urls(self):
        expected = "dQw4w9WgXcQ"
        urls = [
            expected,
            f"https://www.youtube.com/watch?v={expected}",
            f"https://www.youtube.com/watch?v={expected}&t=42s",
            f"https://youtu.be/{expected}?si=test",
            f"https://www.youtube.com/shorts/{expected}",
            f"https://www.youtube.com/embed/{expected}",
            f"https://www.youtube.com/live/{expected}?feature=share",
        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(extract_video_id(url), expected)

    def test_query_plan_includes_core_and_review_people(self):
        people = load_people()
        by_slug = people_by_slug(people)
        self.assertIn("bob-lazar", by_slug)

        queries = build_person_queries(by_slug["jensen-huang"], limit=6)
        self.assertIn('"Jensen Huang" interview', queries)
        self.assertTrue(any("ai infrastructure" in query for query in queries))

        elon_queries = build_person_queries(by_slug["elon-musk"], limit=10)
        self.assertIn('"Elon Musk" Joe Rogan', elon_queries)
        self.assertIn('"Elon Musk" Lex Fridman', elon_queries)
        self.assertIn('"Elon Musk" Tesla AI Day', elon_queries)

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "queries.json"
            plan = write_query_plan([by_slug["bob-lazar"]], output, limit_per_person=3)
            self.assertEqual(plan["people_count"], 1)
            loaded = json.loads(output.read_text())
            self.assertEqual(loaded["people"][0]["slug"], "bob-lazar")
            self.assertEqual(len(loaded["people"][0]["youtube_search_urls"]), 3)

    def test_manual_queue_and_plugin_transcript_export_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            db_path = tmp_path / "queue.sqlite"
            transcripts_dir = tmp_path / "transcripts"
            transcript_file = tmp_path / "plugin.txt"
            transcript_file.write_text("First line.\n\n\nSecond line.", encoding="utf-8")

            person = {
                "name": "Bob Lazar",
                "slug": "bob-lazar",
                "status": "maybe",
                "tier": "C",
                "weight": 1.0,
                "topics": ["interviews"],
            }
            queue = PeopleVideoQueue(db_path)
            output_path = import_plugin_transcript(
                transcript_file=transcript_file,
                video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                person=person,
                title="Bob Lazar Interview",
                channel_name="Example Channel",
                output_dir=transcripts_dir,
                queue=queue,
            )

            data = yaml.safe_load(output_path.read_text())
            self.assertEqual(data["video"]["video_id"], "dQw4w9WgXcQ")
            self.assertEqual(data["video"]["person_slugs"], ["bob-lazar"])
            self.assertEqual(data["transcript"]["full_text"], "First line.\n\nSecond line.")

            stats = queue.stats()
            self.assertEqual(stats["total"], 1)
            self.assertEqual(stats["transcript_ready"], 1)

            export_path = tmp_path / "prioritized.json"
            videos = queue.export_prioritized(export_path, min_tier="C")
            self.assertEqual(len(videos), 1)
            self.assertEqual(videos[0]["transcript_path"], str(output_path))

    def test_existing_queue_record_matching_and_candidate_creation(self):
        person = {
            "name": "Jensen Huang",
            "slug": "jensen-huang",
            "status": "approved",
            "tier": "S",
            "weight": 4.0,
            "sources": [],
        }
        record = {
            "video_id": "abcdefghijk",
            "channel_name": "Acquired",
            "channel_slug": "acquired",
            "title": "Jensen Huang interview on NVIDIA, AI factories, and leadership",
            "upload_date": "2025-01-01",
            "duration": 3600,
            "score": 2,
            "priority": "P3",
            "status": "completed",
            "transcript_path": "",
        }

        self.assertTrue(record_matches_person(record, person))
        with tempfile.TemporaryDirectory() as tmp:
            transcript_dir = Path(tmp)
            transcript = transcript_dir / "abcdefghijk.txt"
            transcript.write_text("Transcript text", encoding="utf-8")
            candidate = candidate_from_existing_record(record, person, transcripts_dir=transcript_dir)

        self.assertEqual(candidate.video_id, "abcdefghijk")
        self.assertEqual(candidate.person_slug, "jensen-huang")
        self.assertEqual(candidate.status, "transcript_ready")
        self.assertEqual(candidate.transcript_path, str(transcript))
        self.assertGreater(source_quality_adjustment(record, person), 0)

        recap_record = {
            **record,
            "title": 'Nvidia CEO SHOCKS Everyone: "China Will WIN The AI Race!"',
            "channel_name": "Ai Grid",
        }
        self.assertLess(source_quality_adjustment(recap_record, person), 0)

    def test_collection_summary_and_report_outputs_next_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            queue = PeopleVideoQueue(tmp_path / "queue.sqlite")
            people = [
                {
                    "name": "Bob Lazar",
                    "slug": "bob-lazar",
                    "status": "maybe",
                    "tier": "C",
                    "line": "manual-review-interview-subjects",
                    "collection_mode": "manual-curation",
                    "weight": 1.0,
                    "topics": ["interviews"],
                    "sources": [],
                },
                {
                    "name": "Jensen Huang",
                    "slug": "jensen-huang",
                    "status": "approved",
                    "tier": "S",
                    "line": "frontier-ai-company-leaders",
                    "collection_mode": "direct-source-first",
                    "weight": 4.0,
                    "topics": ["ai infrastructure"],
                    "sources": [],
                },
            ]
            queue.add_manual_video(
                people[0],
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                title="Bob Lazar Interview",
                channel_name="Example Channel",
            )

            summary = queue.collection_summary(people)
            self.assertEqual(summary["totals"]["people"], 2)
            self.assertEqual(summary["totals"]["with_candidates"], 1)
            self.assertEqual(summary["people"][0]["candidate_count"], 1)
            self.assertEqual(summary["people"][0]["shown_candidate_count"], 1)
            self.assertEqual(summary["people"][0]["next_action"], "import_transcript")
            self.assertEqual(summary["people"][1]["next_action"], "discover_candidates")
            self.assertEqual(next_collection_action(1, 1), "ready_for_extraction")

            json_path = tmp_path / "status.json"
            markdown_path = tmp_path / "status.md"
            write_collection_report(summary, json_path, markdown_path)
            self.assertIn("Bob Lazar", markdown_path.read_text())
            self.assertEqual(json.loads(json_path.read_text())["totals"]["people"], 2)

    def test_search_result_import_extracts_youtube_candidates_from_firecrawl_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = PeopleVideoQueue(Path(tmp) / "queue.sqlite")
            person = {
                "name": "Bob Lazar",
                "slug": "bob-lazar",
                "status": "maybe",
                "tier": "C",
                "weight": 1.0,
                "topics": ["interviews"],
                "sources": [],
            }
            payload = {
                "data": {
                    "web": [
                        {
                            "title": "Joe Rogan Experience #1315 - Bob Lazar & Jeremy Corbell",
                            "url": "https://www.youtube.com/watch?v=BEWz4SXfyCQ",
                            "description": "Long-form interview.",
                        },
                        {
                            "title": "Summary page",
                            "url": "https://example.com/summary",
                            "markdown": "Watch https://youtu.be/dQw4w9WgXcQ for the source.",
                        },
                    ]
                }
            }

            self.assertEqual(
                extract_youtube_urls_from_text("watch https://youtu.be/dQw4w9WgXcQ?t=12"),
                ["https://youtu.be/dQw4w9WgXcQ?t=12"],
            )
            imported = import_search_results(payload, person, queue=queue, source="firecrawl_search")
            self.assertEqual([candidate.video_id for candidate in imported], ["BEWz4SXfyCQ", "dQw4w9WgXcQ"])
            self.assertEqual(queue.stats()["total"], 2)

    def test_batch_search_result_import_infers_person_from_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            queue = PeopleVideoQueue(tmp_path / "queue.sqlite")
            result_file = tmp_path / "bob-lazar-extra.json"
            result_file.write_text(
                json.dumps(
                    {
                        "data": {
                            "web": [
                                {
                                    "title": "Bob Lazar Interview",
                                    "url": "https://www.youtube.com/watch?v=BEWz4SXfyCQ",
                                }
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )
            people = {
                "bob-lazar": {
                    "name": "Bob Lazar",
                    "slug": "bob-lazar",
                    "status": "maybe",
                    "tier": "C",
                    "weight": 1.0,
                    "topics": ["interviews"],
                    "sources": [],
                }
            }

            self.assertEqual(infer_person_slug_from_search_file(result_file, people), "bob-lazar")
            summary = import_search_result_files([result_file], people, queue=queue)
            self.assertEqual(summary["files_processed"], 1)
            self.assertEqual(summary["candidates_imported"], 1)
            self.assertEqual(summary["per_person"]["bob-lazar"], 1)

    def test_batch_plugin_export_import_uses_filename_convention(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            queue = PeopleVideoQueue(tmp_path / "queue.sqlite")
            transcript_file = tmp_path / "bob-lazar__BEWz4SXfyCQ__Joe-Rogan-Experience-1315.txt"
            transcript_file.write_text("Transcript line one.\nTranscript line two.", encoding="utf-8")
            people = {
                "bob-lazar": {
                    "name": "Bob Lazar",
                    "slug": "bob-lazar",
                    "status": "maybe",
                    "tier": "C",
                    "weight": 1.0,
                    "topics": ["interviews"],
                    "sources": [],
                }
            }

            parsed = parse_plugin_export_filename(transcript_file, people)
            self.assertEqual(parsed["person_slug"], "bob-lazar")
            self.assertEqual(parsed["video_id"], "BEWz4SXfyCQ")
            self.assertEqual(parsed["title"], "Joe Rogan Experience 1315")

            summary = import_plugin_export_files(
                [transcript_file],
                people,
                output_dir=tmp_path / "transcripts",
                queue=queue,
            )
            self.assertEqual(summary["files_processed"], 1)
            self.assertEqual(summary["transcripts_imported"], 1)
            self.assertEqual(queue.stats()["transcript_ready"], 1)

    def test_transcript_backlog_report_lists_candidate_filenames(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            queue = PeopleVideoQueue(tmp_path / "queue.sqlite")
            person = {
                "name": "Bob Lazar",
                "slug": "bob-lazar",
                "status": "maybe",
                "tier": "C",
                "weight": 1.0,
                "topics": ["interviews"],
                "sources": [],
            }
            queue.add_manual_video(
                person,
                "https://www.youtube.com/watch?v=BEWz4SXfyCQ",
                title="Joe Rogan Experience #1315 - Bob Lazar & Jeremy Corbell",
                channel_name="PowerfulJRE",
            )
            output = tmp_path / "backlog.md"
            write_transcript_backlog(queue, [person], output, limit=10)
            content = output.read_text()
            self.assertIn("bob-lazar__BEWz4SXfyCQ__", content)
            self.assertIn("Joe Rogan Experience #1315", content)


if __name__ == "__main__":
    unittest.main()
