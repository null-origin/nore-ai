# src/nore_ai/cli/main.py
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from ..engine.pipeline import run_day_pipeline


def _load_config(path: Path) -> Dict[str, Any]:
    """
    Load a config file for the pipeline (JSON).
    """
    text = path.read_text(encoding="utf-8")
    return json.loads(text)


def _build_config_from_events(events_path: Path) -> Dict[str, Any]:
    """
    Build a minimal config dict when the user passes --events directly.
    """
    return {
        "events_path": str(events_path),
        "event_schema": "schemas/event.schema.json",  # relative to repo root when running
        "validate": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="nore-ai",
        description="NORE-AI command-line interface",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- run-day subcommand ---
    run_day_parser = subparsers.add_parser(
        "run-day",
        help="Run the NORE-AI pipeline for a single day",
    )

    # Option A: config file (positional, optional)
    run_day_parser.add_argument(
        "config",
        type=Path,
        nargs="?",
        help="Path to a JSON config file (includes events_path, event_schema, etc.)",
    )

    # Option B: direct events file
    run_day_parser.add_argument(
        "--events",
        "-e",
        type=Path,
        help="Path to a JSONL events file (bypasses config file)",
    )

    args = parser.parse_args()

    if args.command == "run-day":
        # Prefer --events if provided
        if args.events is not None:
            config = _build_config_from_events(args.events)
        else:
            if args.config is None:
                parser.error("run-day requires either --events/-e or a config path")
            config = _load_config(args.config)

        events, errors = run_day_pipeline(config)

        total_valid = len(events)
        total_errors = len(errors)

        print("[nore-ai] run-day completed")
        print(f"  valid events     : {total_valid}")
        print(f"  validation errors: {total_errors}")

        if total_errors:
            print("  first few errors:")
            for err in errors[:5]:
                print(f"    - {err}")
