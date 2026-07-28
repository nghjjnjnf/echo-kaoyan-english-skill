#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import re
import uuid
from pathlib import Path


def default_exercises_dir():
    return Path.home() / ".codex" / "kaoyan-english" / "exercises"


def read_text_arg(value):
    if not value:
        return ""
    path = Path(value)
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return value


def read_json_arg(value):
    if not value:
        return {}
    stripped = value.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        return json.loads(stripped)
    path = Path(value)
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(stripped)


def slugify(value):
    value = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff_-]+", "-", value or "").strip("-")
    return value[:80] or "exercise"


def write_markdown(exercise, path):
    content = f"""# {exercise["title"]}

## 元信息
- 练习 ID：{exercise["exercise_id"]}
- 创建时间：{exercise["created_at"]}
- 题型：{exercise["task_type"]}
- 难度：{exercise.get("difficulty") or "unspecified"}
- 来源：{exercise.get("source_url") or "local/generated"}
- 练习模式：首次展示时隐藏答案和解析

## 原文

{exercise.get("passage", "").strip()}

## 题目

{exercise.get("questions", "").strip()}

## 标准答案

本节供后续解析读取；练习首次展示时不要直接暴露给用户。
```json
{json.dumps(exercise.get("answer_key", {}), ensure_ascii=False, indent=2)}
```

## 难度映射

```json
{json.dumps(exercise.get("difficulty_map", {}), ensure_ascii=False, indent=2)}
```

## 证据映射

```json
{json.dumps(exercise.get("evidence_map", {}), ensure_ascii=False, indent=2)}
```
"""
    path.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Save a generated kaoyan English practice exercise before the user answers.")
    parser.add_argument("--exercises-dir", default=str(default_exercises_dir()))
    parser.add_argument("--title", default="考研英语模拟练习")
    parser.add_argument("--task-type", choices=["reading", "cloze"], required=True)
    parser.add_argument("--difficulty")
    parser.add_argument("--source-url")
    parser.add_argument("--source-mode")
    parser.add_argument("--passage", help="Passage text or path to a UTF-8 text file.")
    parser.add_argument("--questions", help="Questions text or path to a UTF-8 text file.")
    parser.add_argument("--answer-key", help="JSON string or path.")
    parser.add_argument("--difficulty-map", help="JSON string or path. Use medium/hard labels for at least 30% of items.")
    parser.add_argument("--evidence-map", help="JSON string or path.")
    args = parser.parse_args()

    created_at = dt.datetime.now().isoformat(timespec="seconds")
    exercise = {
        "exercise_id": uuid.uuid4().hex[:12],
        "created_at": created_at,
        "title": args.title,
        "task_type": args.task_type,
        "difficulty": args.difficulty,
        "source_url": args.source_url,
        "source_mode": args.source_mode or ("local_original" if not args.source_url else "external"),
        "passage": read_text_arg(args.passage),
        "questions": read_text_arg(args.questions),
        "answer_key": read_json_arg(args.answer_key),
        "difficulty_map": read_json_arg(args.difficulty_map),
        "evidence_map": read_json_arg(args.evidence_map),
    }

    target_dir = Path(args.exercises_dir).expanduser()
    target_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{created_at[:10]}-{slugify(args.title)}-{exercise['exercise_id']}"
    json_path = target_dir / f"{stem}.json"
    md_path = target_dir / f"{stem}.md"
    json_path.write_text(json.dumps(exercise, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(exercise, md_path)
    print(f"exercise_id={exercise['exercise_id']}")
    print(f"json={json_path}")
    print(f"markdown={md_path}")


if __name__ == "__main__":
    main()
