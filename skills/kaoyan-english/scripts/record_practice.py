#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path


def slugify(value):
    value = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff_-]+", "-", value).strip("-")
    return value[:80] or "practice"


def default_records_dir():
    return Path.home() / ".codex" / "kaoyan-english" / "practice-records"


def read_json_arg(value):
    path = Path(value)
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(value)


def write_markdown(record, path):
    answers = record.get("user_answers", {})
    answer_lines = "\n".join(f"- {key}: {value}" for key, value in answers.items()) or "- 暂无"
    answer_key = record.get("answer_key", {})
    answer_key_lines = "\n".join(f"- {key}: {value}" for key, value in answer_key.items()) or "- 暂无"
    title = record.get("title") or record.get("topic") or "考研英语模拟练习"
    content = f"""# {title}

## 记录信息

- 记录时间：{record.get("created_at")}
- 题型：{record.get("task_type", "unknown")}
- 难度：{record.get("difficulty", "unspecified")}
- 来源：{record.get("source_url", "local/generated")}

## 原文

{record.get("passage", "").strip()}

## 题目

{record.get("questions", "").strip()}

## 用户答案

{answer_lines}

## 标准答案

{answer_key_lines}

## 解析

{record.get("analysis", "").strip()}
"""
    path.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Save a kaoyan English simulation practice record locally.")
    parser.add_argument("--record-json", help="JSON string or path containing the full record.")
    parser.add_argument("--records-dir", default=str(default_records_dir()))
    parser.add_argument("--title")
    parser.add_argument("--task-type", choices=["reading", "cloze"], default="reading")
    parser.add_argument("--difficulty")
    parser.add_argument("--source-url")
    parser.add_argument("--passage-file")
    parser.add_argument("--questions-file")
    parser.add_argument("--analysis-file")
    parser.add_argument("--user-answers", help='JSON string or file, for example {"1":"A","2":"C"}.')
    args = parser.parse_args()

    if args.record_json:
        record = read_json_arg(args.record_json)
    else:
        record = {
            "title": args.title,
            "task_type": args.task_type,
            "difficulty": args.difficulty,
            "source_url": args.source_url,
            "passage": Path(args.passage_file).read_text(encoding="utf-8") if args.passage_file else "",
            "questions": Path(args.questions_file).read_text(encoding="utf-8") if args.questions_file else "",
            "analysis": Path(args.analysis_file).read_text(encoding="utf-8") if args.analysis_file else "",
            "user_answers": read_json_arg(args.user_answers) if args.user_answers else {},
        }

    created_at = record.get("created_at") or dt.datetime.now().isoformat(timespec="seconds")
    record["created_at"] = created_at
    records_dir = Path(args.records_dir).expanduser()
    records_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{created_at[:10]}-{slugify(record.get('title') or record.get('task_type') or 'practice')}"
    json_path = records_dir / f"{stem}.json"
    md_path = records_dir / f"{stem}.md"
    counter = 1
    while json_path.exists() or md_path.exists():
        json_path = records_dir / f"{stem}-{counter}.json"
        md_path = records_dir / f"{stem}-{counter}.md"
        counter += 1

    json_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(record, md_path)
    print(f"json={json_path}")
    print(f"markdown={md_path}")


if __name__ == "__main__":
    main()
