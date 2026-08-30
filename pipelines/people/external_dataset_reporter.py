#!/usr/bin/env python3
"""Render a compact status report for external people dataset candidates."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any
import re

import yaml

ROOT = Path("/Users/shaansisodia/SISO_Workspace/SISO_Knowledge")
DATASET_REGISTRY = ROOT / "pipelines" / "people" / "external_datasets.yaml"
REPORT_PATH = ROOT / "pipelines" / "people" / "external_dataset_status.md"

COUNT_PATTERN = re.compile(
    r"(?P<count>\d[\d,.]*(?:\s*(?:K|M|B|k|m|b|\+|mn|million|billion))?)\s+"
    r"(?P<unit>rows?|episodes?|transcripts?|podcasts?|quotes?|people|persons|"
    r"leaders?|entities|files?|videos?|shows?|sources?|credits?|charts?|"
    r"conversations?|datasets?)",
    re.IGNORECASE,
)


def load_external_datasets(path: Path = DATASET_REGISTRY) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def render_data_volume(dataset: dict[str, Any]) -> str:
    volume = dataset.get("data_volume")
    if isinstance(volume, dict):
        count = volume.get("count", "unknown")
        unit = volume.get("unit", "items")
        qualifier = volume.get("qualifier")
        if qualifier:
            return f"{count} {unit} ({qualifier})"
        return f"{count} {unit}"

    if isinstance(volume, str) and volume:
        return volume

    searchable = " ".join(
        str(part)
        for part in [
            dataset.get("freshness_notes", ""),
            " ".join(dataset.get("coverage_notes", [])),
        ]
    )
    matches = COUNT_PATTERN.findall(searchable)
    if not matches:
        return "unknown"

    rendered = []
    seen = set()
    for count, unit in matches[:3]:
        key = (count, unit.lower())
        if key in seen:
            continue
        seen.add(key)
        rendered.append(f"{count} {unit}")
    return "; ".join(rendered)


def render_status(data: dict[str, Any]) -> str:
    datasets = data["datasets"]
    by_status = Counter(dataset["status"] for dataset in datasets)
    by_type = Counter(dataset["source_type"] for dataset in datasets)

    lines = [
        "# External Dataset Status",
        "",
        f"Generated: `{data['generated_at']}`",
        f"Datasets tracked: `{len(datasets)}`",
        "",
        "## Status Counts",
        "",
    ]
    for status, count in sorted(by_status.items()):
        lines.append(f"- `{status}`: `{count}`")

    lines.extend(["", "## Source Types", ""])
    for source_type, count in sorted(by_type.items()):
        lines.append(f"- `{source_type}`: `{count}`")

    lines.extend(["", "## P0 Import Candidates", ""])
    for dataset in datasets:
        if dataset["status"] != "p0_import_candidate":
            continue
        people = ", ".join(dataset.get("mapped_people", [])[:8])
        lines.extend(
            [
                f"### {dataset['name']}",
                "",
                f"- URL: {dataset['url']}",
                f"- Type: `{dataset['source_type']}`",
                f"- Platform: `{dataset['platform']}`",
                f"- License observed: `{dataset['license_observed']}`",
                f"- Observed at: `{dataset.get('observed_at', data.get('last_checked_at', 'unknown'))}`",
                f"- Source last updated: `{dataset.get('source_last_updated', 'unknown')}`",
                f"- Data coverage: `{dataset.get('data_coverage_start', 'unknown')}` to `{dataset.get('data_coverage_end', 'unknown')}`",
                f"- Data volume: `{render_data_volume(dataset)}`",
                f"- Freshness notes: {dataset.get('freshness_notes', 'unknown')}",
                f"- Mapped people: {people}",
                f"- Import strategy: {dataset['import_strategy']}",
                "",
            ]
        )

    lines.extend(["## Data Volume Inventory", ""])
    lines.append("| Dataset | Status | Source type | Data volume | Freshness |")
    lines.append("|---|---:|---|---:|---|")
    for dataset in datasets:
        lines.append(
            "| "
            + " | ".join(
                [
                    dataset["id"],
                    dataset["status"],
                    dataset["source_type"],
                    render_data_volume(dataset),
                    str(dataset.get("source_last_updated", "unknown")),
                ]
            )
            + " |"
        )
    lines.append("")

    lines.extend(["## Gaps", ""])
    for dataset in datasets:
        if dataset["status"] == "blocked":
            lines.append(f"- `{dataset['id']}`: {dataset['coverage_notes'][0]}")

    return "\n".join(lines).rstrip() + "\n"


def write_status_report(
    registry_path: Path = DATASET_REGISTRY,
    report_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    data = load_external_datasets(registry_path)
    report_path.write_text(render_status(data), encoding="utf-8")
    return {
        "dataset_count": len(data["datasets"]),
        "report_path": str(report_path),
    }


def main() -> None:
    result = write_status_report()
    print(f"Wrote {result['dataset_count']} dataset candidates to {result['report_path']}")


if __name__ == "__main__":
    main()
