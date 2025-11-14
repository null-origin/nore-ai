from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List


def read_jsonl(path: Path) -> Iterator[Dict[str, Any]]:
    """
    Stream JSON objects from a .jsonl file.
    """
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def write_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    """
    Write an iterable of JSON-serializable dicts to a .jsonl file.
    """
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_schema(path: Path) -> Dict[str, Any]:
    """
    Load a JSON Schema document.
    """
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
