#!/usr/bin/env python3
"""
YouTube Pipeline Orchestrator

Runs the complete YouTube-to-library pipeline:
1. Run prioritize.py to get Tier A/B videos
2. Extract insights from each video
3. Synthesize pages into books
4. Rebuild library index
5. Run concept linker

Usage:
    python3 pipelines/youtube/run_pipeline.py           # incremental (skip done)
    python3 pipelines/youtube/run_pipeline.py --full    # re-do all
    python3 pipelines/youtube/run_pipeline.py --dry-run  # show what would happen
    python3 pipelines/youtube/run_pipeline.py --steps 1,2  # run only specific steps
"""
import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path("/Users/shaansisodia/SISO_Library")
PIPELINE_DIR = ROOT / "pipelines" / "youtube"


def run_command(cmd: list[str], description: str, dry_run: bool = False) -> dict:
    """Run a command and return result."""
    print(f"\n{'='*60}")
    print(f"Step: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")

    if dry_run:
        print("[DRY RUN] Would execute above command")
        return {"status": "dry_run", "command": cmd}

    try:
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
        )

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"STDERR: {result.stderr}", file=sys.stderr)

        return {
            "status": "success" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except subprocess.TimeoutExpired:
        print(f"ERROR: Command timed out after 600 seconds")
        return {"status": "timeout", "command": cmd}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"status": "error", "error": str(e)}


def run_step(step: int, args) -> dict:
    """Run a single pipeline step."""
    dry_run = args.dry_run

    if step == 1:
        # Step 1: Prioritize videos
        cmd = [
            sys.executable,
            str(PIPELINE_DIR / "prioritize.py"),
            "--min-tier", args.min_tier,
            "--limit", str(args.limit),
            "--output", args.prioritized_file,
        ]
        return run_command(cmd, "1. Prioritize videos (Tier A/B)", dry_run)

    elif step == 2:
        # Step 2: Extract insights
        cmd = [
            sys.executable,
            str(PIPELINE_DIR / "extract_prioritized.py"),
            "--input", args.prioritized_file,
            "--workers", str(args.workers),
        ]
        if args.limit > 0:
            cmd.extend(["--limit", str(args.limit)])
        return run_command(cmd, "2. Extract insights from prioritized videos", dry_run)

    elif step == 3:
        # Step 3: Synthesize into books
        cmd = [
            sys.executable,
            str(PIPELINE_DIR / "synthesize.py"),
        ]
        if args.shelf:
            cmd.extend(["--shelf", args.shelf])
        return run_command(cmd, "3. Synthesize video pages into books", dry_run)

    elif step == 4:
        # Step 4: Rebuild index
        cmd = [
            sys.executable,
            str(ROOT / "queries" / "rebuild_index.py"),
        ]
        return run_command(cmd, "4. Rebuild library index", dry_run)

    elif step == 5:
        # Step 5: Run concept linker
        cmd = [
            sys.executable,
            str(PIPELINE_DIR / "concept_linker.py"),
        ]
        return run_command(cmd, "5. Run concept linker", dry_run)

    else:
        return {"status": "error", "error": f"Unknown step: {step}"}


def main():
    parser = argparse.ArgumentParser(description="YouTube Pipeline Orchestrator")
    parser.add_argument("--incremental", action="store_true",
                       help="Skip already-processed videos (default)")
    parser.add_argument("--full", action="store_true",
                       help="Re-do all videos (ignore already-processed)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would happen without executing")
    parser.add_argument("--steps", type=str, default="1,2,3,4,5",
                       help="Comma-separated steps to run (default: 1,2,3,4,5)")
    parser.add_argument("--min-tier", choices=["A", "B", "C"], default="B",
                       help="Minimum tier to process (default: B)")
    parser.add_argument("--limit", type=int, default=0,
                       help="Limit videos per step (0=all)")
    parser.add_argument("--workers", type=int, default=2,
                       help="Parallel workers for extraction (default: 2)")
    parser.add_argument("--shelf", type=str, default="",
                       help="Shelf to synthesize (default: auto-detect)")
    parser.add_argument("--prioritized-file", type=str, default="/tmp/youtube-prioritized.json",
                       help="Output file for prioritized list")
    args = parser.parse_args()

    print(f"{'='*60}")
    print(f"YouTube Pipeline Runner")
    print(f"Started: {datetime.now().isoformat()}")
    print(f"{'='*60}")
    print(f"Mode: {'FULL' if args.full else 'INCREMENTAL'}")
    print(f"Steps: {args.steps}")
    print(f"Min tier: {args.min_tier}")
    if args.limit > 0:
        print(f"Limit: {args.limit} videos")

    # Parse steps
    step_list = [int(s.strip()) for s in args.steps.split(",") if s.strip()]
    valid_steps = {1, 2, 3, 4, 5}
    step_list = [s for s in step_list if s in valid_steps]

    if not step_list:
        print("ERROR: No valid steps specified")
        sys.exit(1)

    print(f"Running steps: {step_list}")

    # Run steps
    results = {}
    for step in step_list:
        result = run_step(step, args)
        results[step] = result

        if result.get("status") == "error" and not args.dry_run:
            print(f"\nERROR at step {step}: {result.get('error', 'Unknown error')}")
            print("Stopping pipeline.")
            break

        if result.get("status") == "timeout":
            print(f"\nTIMEOUT at step {step}")
            print("Stopping pipeline.")
            break

    # Summary
    print(f"\n{'='*60}")
    print(f"Pipeline Summary")
    print(f"{'='*60}")

    success = sum(1 for r in results.values() if r.get("status") == "success")
    errors = sum(1 for r in results.values() if r.get("status") == "error")

    for step, result in results.items():
        status = result.get("status", "unknown")
        step_names = {
            1: "Prioritize",
            2: "Extract",
            3: "Synthesize",
            4: "Rebuild Index",
            5: "Concept Linker",
        }
        print(f"  Step {step} ({step_names.get(step, step)}): {status}")

    print(f"\nTotal: {success} success, {errors} errors")
    print(f"Completed: {datetime.now().isoformat()}")

    if errors > 0 and not args.dry_run:
        print("\nPipeline completed with errors.")
        sys.exit(1)
    else:
        print("\nPipeline completed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
