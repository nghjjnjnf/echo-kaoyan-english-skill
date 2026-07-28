#!/usr/bin/env python3
import argparse
import json
import math
import re
import sys
from pathlib import Path


ERRORS = []
CHALLENGING_LEVELS = {"medium", "hard", "difficult", "challenging", "中", "难", "中等", "困难", "较难"}


def require(condition, message):
    if not condition:
        ERRORS.append(message)


def word_count(text):
    return len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text))


def count_questions(text):
    return len(re.findall(r"(?m)^\s*\d+[\.)]\s+", text))


def count_option_groups(text):
    return len(re.findall(r"(?ms)^\s*\[A\].*?^\s*\[B\].*?^\s*\[C\].*?^\s*\[D\]", text))


def count_blanks(text):
    return len(re.findall(r"_{2,}\s*\d*\s*_{2,}|__+\s*\d+\s*__+|\(\s*\d+\s*\)", text))


def normalize_level(value):
    if isinstance(value, dict):
        value = value.get("level") or value.get("difficulty") or ""
    return str(value).strip().lower()


def challenging_count(difficulty_map):
    if not isinstance(difficulty_map, dict):
        return 0
    return sum(1 for value in difficulty_map.values() if normalize_level(value) in CHALLENGING_LEVELS)


def validate_difficulty_map(data, item_count):
    difficulty_map = data.get("difficulty_map", {})
    require(isinstance(difficulty_map, dict) and len(difficulty_map) == item_count, f"difficulty_map must contain {item_count} item difficulty labels")
    required = math.ceil(item_count * 0.3)
    got = challenging_count(difficulty_map)
    require(got >= required, f"at least 30% of items must be medium/hard difficulty, need {required}, got {got}")


def validate_exercise(data):
    task_type = data.get("task_type")
    passage = data.get("passage", "")
    questions = data.get("questions", "")
    answer_key = data.get("answer_key", {})
    wc = word_count(passage)

    require(task_type in {"reading", "cloze"}, "task_type must be reading or cloze")
    if task_type == "reading":
        require(450 <= wc <= 550, f"reading passage word count must be 450-550, got {wc}")
        require(count_questions(questions) == 5, "reading exercise must contain 5 questions")
        require(count_option_groups(questions) == 5, "reading exercise must contain 5 complete A-D option groups")
        require(len(answer_key) == 5, "reading answer_key must contain 5 answers")
        validate_difficulty_map(data, 5)
    elif task_type == "cloze":
        require(300 <= wc <= 350, f"cloze passage word count must be 300-350, got {wc}")
        blank_count = count_blanks(passage)
        require(blank_count in {10, 20}, f"cloze passage must contain 10 or 20 blanks, got {blank_count}")
        require(len(answer_key) == blank_count, "cloze answer_key count must match blank count")
        validate_difficulty_map(data, blank_count)

    leakage_patterns = (r"(?i)\banswer\s*key\b", r"(?i)\banswers?\s*:", r"答案", r"解析")
    for pattern in leakage_patterns:
        require(not re.search(pattern, questions), f"questions appear to leak answer/explanation marker: {pattern}")


def main():
    parser = argparse.ArgumentParser(description="Validate a generated kaoyan English practice exercise JSON.")
    parser.add_argument("exercise_json")
    args = parser.parse_args()

    data = json.loads(Path(args.exercise_json).read_text(encoding="utf-8"))
    validate_exercise(data)
    if ERRORS:
        for error in ERRORS:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Generated exercise validation passed.")


if __name__ == "__main__":
    main()
