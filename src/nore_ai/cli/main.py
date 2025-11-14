# src/nore_ai/cli/main.py
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from ..engine.pipeline import run_day_pipeline


def _load_config(path: Path) -> Dict[str, Any]:
    """
    Load a config file for the pipeline.

    For now we assume JSON; YAML can be added later if needed.
    """
    text = path.read_text(encoding="utf-8")
    return json.loads(text)


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
    run_day_parser.add_argument(
        "config",
        type=Path,
        help="Path to a JSON config file (includes events_path, event_schema, etc.)",
    )

    args = parser.parse_args()

    if args.command == "run-day":
        config_path: Path = args.config
        config = _load_config(config_path)

        events, errors = run_day_pipeline(config)

        total_valid = len(events)
        total_errors = len(errors)

        print(f"[nore-ai] run-day completed")
        print(f"  valid events     : {total_valid}")
        print(f"  validation errors: {total_errors}")

        if total_errors:
            print("  first few errors:")
            for err in errors[:5]:
                print(f"    - {err}")
