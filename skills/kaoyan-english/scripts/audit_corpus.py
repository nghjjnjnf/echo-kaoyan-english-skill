#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


ERRORS = []


def require(condition, message):
    if not condition:
        ERRORS.append(message)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def audit_year(year_dir):
    meta = load_json(year_dir / "meta.json")
    qmap = load_json(year_dir / "question-map.json")
    answers = load_json(year_dir / "answers.json").get("answers", {})
    sections = set(meta.get("sections", []))

    for section in ("cloze", "translation", "writing"):
        require(section in sections, f"{year_dir}: missing section {section}")

    for idx in range(1, 5):
        section = f"reading-text-{idx}"
        require(section in sections, f"{year_dir}: missing {section}")
        mapped = [q for q, item in qmap.items() if item.get("section") == section]
        require(len(mapped) == 5, f"{year_dir}: {section} should map 5 questions, got {len(mapped)}")
        section_answers = answers.get(section, {})
        for question in mapped:
            require(question in section_answers, f"{year_dir}: missing answer for question {question}")

    cloze_mapped = [q for q, item in qmap.items() if item.get("section") == "cloze"]
    require(len(cloze_mapped) in {0, 20}, f"{year_dir}: cloze should map 20 questions when present, got {len(cloze_mapped)}")
    for question in cloze_mapped:
        require(question in answers.get("cloze", {}), f"{year_dir}: missing cloze answer {question}")

    for item in qmap.values():
        file_name = item.get("file")
        if file_name:
            require((year_dir / file_name).is_file(), f"{year_dir}: mapped file missing: {file_name}")


def main():
    parser = argparse.ArgumentParser(description="Audit kaoyan English corpus shape and answer coverage.")
    parser.add_argument("--skill", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--exam", choices=["english-i", "english-ii"])
    parser.add_argument("--year")
    args = parser.parse_args()

    root = Path(args.skill) / "references" / "papers"
    exams = [args.exam] if args.exam else ["english-i", "english-ii"]
    for exam in exams:
        exam_dir = root / exam
        years = [args.year] if args.year else sorted(path.name for path in exam_dir.iterdir() if path.is_dir())
        for year in years:
            audit_year(exam_dir / str(year))

    if ERRORS:
        for error in ERRORS:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Corpus audit passed.")


if __name__ == "__main__":
    main()
