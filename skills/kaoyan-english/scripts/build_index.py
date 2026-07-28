#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


SECTION_LABELS = {
    "cloze": "Section I Use of English",
    "reading-text-1": "Reading Text 1",
    "reading-text-2": "Reading Text 2",
    "reading-text-3": "Reading Text 3",
    "reading-text-4": "Reading Text 4",
    "new-question-type": "New Question Type",
    "translation": "Translation",
    "writing": "Writing",
}


def load_json(path, default=None):
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def question_id(exam, year, section, question):
    return f"{exam}-{year}-{section}-q{question}"


def build_index(skill):
    references = skill / "references"
    corpus_index_path = references / "corpus-index.json"
    corpus_index = load_json(corpus_index_path, {})
    index = {
        "version": 1,
        "source": "references/corpus-index.json",
        "description": "Direct lookup index for exam/year/section/question corpus routing.",
        "exams": {},
    }

    for exam, years in sorted(corpus_index.items()):
        exam_entry = {"years": {}}
        for year, year_info in sorted(years.items(), key=lambda item: int(item[0])):
            year_dir = references / "papers" / exam / str(year)
            qmap = load_json(year_dir / "question-map.json", {})
            answers = load_json(year_dir / "answers.json", {}).get("answers", {})
            sections = year_info.get("sections", [])
            year_entry = {
                "path": f"references/papers/{exam}/{year}",
                "sections": {},
                "questions": {},
            }

            for section in sections:
                filename = f"{section}.md"
                section_entry = {
                    "label": SECTION_LABELS.get(section, section),
                    "file": filename,
                    "path": f"references/papers/{exam}/{year}/{filename}",
                    "questions": {},
                }
                for question, item in sorted(qmap.items(), key=lambda item: int(item[0])):
                    if item.get("section") != section:
                        continue
                    question_entry = {
                        "id": question_id(exam, year, section, question),
                        "exam": exam,
                        "year": int(year),
                        "section": section,
                        "question": int(question),
                        "file": item.get("file", filename),
                        "path": f"references/papers/{exam}/{year}/{item.get('file', filename)}",
                    }
                    answer = answers.get(section, {}).get(str(question))
                    if answer is not None:
                        question_entry["answer"] = answer
                    section_entry["questions"][question] = question_entry
                    year_entry["questions"][question] = question_entry

                section_entry["question_count"] = len(section_entry["questions"])
                year_entry["sections"][section] = section_entry

            year_entry["question_count"] = len(year_entry["questions"])
            exam_entry["years"][str(year)] = year_entry
        index["exams"][exam] = exam_entry
    return index


def main():
    parser = argparse.ArgumentParser(description="Build references/index.json for fast corpus lookup.")
    parser.add_argument("--skill", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    skill = Path(args.skill)
    output = Path(args.output) if args.output else skill / "references" / "index.json"
    index = build_index(skill)
    output.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    question_count = sum(
        year_entry.get("question_count", 0)
        for exam_entry in index["exams"].values()
        for year_entry in exam_entry["years"].values()
    )
    print(f"index={output}")
    print(f"questions={question_count}")


if __name__ == "__main__":
    main()
