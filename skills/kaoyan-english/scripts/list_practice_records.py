#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def default_records_dir():
    return Path.home() / ".codex" / "kaoyan-english" / "practice-records"


def main():
    parser = argparse.ArgumentParser(description="List saved kaoyan English practice records.")
    parser.add_argument("--records-dir", default=str(default_records_dir()))
    parser.add_argument("--task-type", choices=["reading", "cloze"])
    args = parser.parse_args()

    records_dir = Path(args.records_dir).expanduser()
    if not records_dir.exists():
        print(f"No records directory: {records_dir}")
        return

    rows = []
    for path in sorted(records_dir.glob("*.json"), reverse=True):
        data = json.loads(path.read_text(encoding="utf-8"))
        if args.task_type and data.get("task_type") != args.task_type:
            continue
        rows.append((data.get("created_at", ""), data.get("task_type", ""), data.get("title", ""), path))

    for created_at, task_type, title, path in rows:
        print(f"{created_at}\t{task_type}\t{title}\t{path}")


if __name__ == "__main__":
    main()
