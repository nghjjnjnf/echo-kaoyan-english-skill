#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def print_from_index(skill, exam, year, question=None, section=None):
    index_path = skill / "references" / "index.json"
    if not index_path.is_file():
        return False
    index = load_json(index_path)
    year_entry = index.get("exams", {}).get(exam, {}).get("years", {}).get(str(year))
    if not year_entry:
        return False

    year_dir = skill / year_entry["path"]
    print(f"year_dir={year_dir}")
    print(f"sections={', '.join(year_entry.get('sections', {}).keys())}")

    if question:
        item = year_entry.get("questions", {}).get(str(question))
        if not item:
            raise SystemExit(f"Question {question} not found in {index_path}")
        print(f"question={question}")
        print(f"section={item['section']}")
        print(f"file={skill / item['path']}")
        if "answer" in item:
            print(f"answer={item['answer']}")

    if section:
        item = year_entry.get("sections", {}).get(section)
        if not item:
            raise SystemExit(f"Section {section} not found in {index_path}")
        print(f"file={skill / item['path']}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Locate kaoyan English paper resources.")
    parser.add_argument("--skill", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--exam", default="english-i")
    parser.add_argument("--year", required=True)
    parser.add_argument("--question")
    parser.add_argument("--section")
    args = parser.parse_args()

    skill = Path(args.skill)
    if print_from_index(skill, args.exam, args.year, args.question, args.section):
        return

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
