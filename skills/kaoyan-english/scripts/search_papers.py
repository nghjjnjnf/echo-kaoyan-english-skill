#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Locate kaoyan English paper resources.")
    parser.add_argument("--skill", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--exam", default="english-i")
    parser.add_argument("--year", required=True)
    parser.add_argument("--question")
    parser.add_argument("--section")
    args = parser.parse_args()

    skill = Path(args.skill)
    year_dir = skill / "references" / "papers" / args.exam / str(args.year)
    if not year_dir.exists():
        raise SystemExit(f"Missing year directory: {year_dir}")

    print(f"year_dir={year_dir}")
    meta = load_json(year_dir / "meta.json")
    print(f"sections={', '.join(meta.get('sections', []))}")

    if args.question:
        qmap = load_json(year_dir / "question-map.json")
        item = qmap.get(str(args.question))
        if not item:
            raise SystemExit(f"Question {args.question} not found in {year_dir / 'question-map.json'}")
        print(f"question={args.question}")
        print(f"section={item['section']}")
        print(f"file={year_dir / item['file']}")
        answers = load_json(year_dir / "answers.json")
        answer = answers.get("answers", {}).get(item["section"], {}).get(str(args.question))
        if answer is not None:
            print(f"answer={answer}")

    if args.section:
        filename = args.section if args.section.endswith(".md") else f"{args.section}.md"
        print(f"file={year_dir / filename}")


if __name__ == "__main__":
    main()
