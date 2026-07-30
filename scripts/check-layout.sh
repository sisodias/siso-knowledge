#!/usr/bin/env bash
set -euo pipefail

domain_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
workspace_root="$(cd "$domain_root/.." && pwd)"

python3 - "$domain_root" "$workspace_root" <<'PY'
import json
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
workspace = pathlib.Path(sys.argv[2])
manifest = json.loads((root / "DOMAIN-MANIFEST.json").read_text())
errors = []

for zone in manifest["zones"]:
    if not (root / zone["path"]).exists():
        errors.append(f"required zone missing: {zone['path']}")

for forbidden in manifest["forbidden_top_level"]:
    if (root / forbidden).exists():
        errors.append(f"forbidden top-level path exists: {forbidden}")

old_path = workspace / "SISO_Library"
if old_path.exists() or old_path.is_symlink():
    errors.append("retired SISO_Library compatibility path exists")

for work in manifest["research_works"]:
    path = root / work["path"]
    if not (path / ".git").is_dir():
        errors.append(f"Research Work is not an independent Git checkout: {work['path']}")
        continue
    remote = subprocess.run(
        ["git", "-C", str(path), "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    if remote != work["remote"]:
        errors.append(f"Research Work origin mismatch: {work['path']} -> {remote!r}")

for exception in manifest["boundary_exceptions"]:
    if not (root / exception["path"]).exists():
        errors.append(f"declared boundary exception missing without migration receipt: {exception['path']}")

tracked = subprocess.run(
    ["git", "-C", str(root), "ls-files"], capture_output=True, text=True, check=True
).stdout.splitlines()
personal_root = "/" + "Users" + "/" + "shaansisodia"
absolute = subprocess.run(
    ["git", "-C", str(root), "grep", "--cached", "-Il", personal_root],
    capture_output=True,
    text=True,
).stdout.splitlines()
runtime_pattern = re.compile(r"(^|/)(inbox|outbox|memory|heartbeat|workspace)/|\.(sqlite|db|log|jsonl)$")
runtime_like = [path for path in tracked if runtime_pattern.search(path)]
index_entries = subprocess.run(
    ["git", "-C", str(root), "ls-files", "-s"],
    capture_output=True,
    text=True,
    check=True,
).stdout.splitlines()
symlinks = [entry for entry in index_entries if entry.startswith("120000 ")]

baseline = manifest["debt_baseline"]
if len(absolute) > baseline["tracked_files_with_personal_absolute_paths_max"]:
    errors.append(f"absolute-path debt increased: {len(absolute)} > {baseline['tracked_files_with_personal_absolute_paths_max']}")
if len(runtime_like) > baseline["tracked_runtime_or_data_looking_files_max"]:
    errors.append(f"tracked runtime/data debt increased: {len(runtime_like)} > {baseline['tracked_runtime_or_data_looking_files_max']}")
if len(symlinks) > baseline["compatibility_symlinks_inside_domain_max"]:
    errors.append(f"symlink debt increased: {len(symlinks)} > {baseline['compatibility_symlinks_inside_domain_max']}")

if errors:
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"PASS: {len(manifest['zones'])} declared Knowledge zones exist")
print(f"PASS: {len(manifest['research_works'])} Research Works have independent matching Git origins")
print("PASS: retired and superseded top-level paths are absent")
print(f"PASS: debt ratchets hold (absolute paths={len(absolute)}, runtime/data-looking={len(runtime_like)}, symlinks={len(symlinks)})")
PY

for data_path in \
  pipelines/people/corpus/ \
  pipelines/people/raw_sources/ \
  pipelines/people/dossiers/ \
  pipelines/people/source_plans/ \
  pipelines/youtube/inbox/ \
  pipelines/youtube/reports/ \
  pipelines/youtube/search_results/ \
  pipelines/youtube/transcripts/ \
  pipelines/youtube/people_video_queue.sqlite \
  _index/events.jsonl \
  _index/agent-status.json; do
  if ! git -C "$domain_root" check-ignore -q "$data_path"; then
    printf 'FAIL: local data-plane path is not ignored: %s\n' "$data_path" >&2
    exit 1
  fi
done

printf 'PASS: declared local data-plane paths are ignored\n'
printf 'SISO Knowledge layout: verified\n'
