#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Review wrong answers in a saved practice record.")
    parser.add_argument("record_json")
    args = parser.parse_args()

    data = json.loads(Path(args.record_json).read_text(encoding="utf-8"))
    user_answers = {str(k): str(v).upper() for k, v in data.get("user_answers", {}).items()}
    answer_key = {str(k): str(v).upper() for k, v in data.get("answer_key", {}).items()}
    wrong = []
    for key, answer in answer_key.items():
        user_answer = user_answers.get(key, "")
        if user_answer != answer:
            wrong.append((key, user_answer or "未作答", answer))

    print(f"title={data.get('title', '')}")
    print(f"task_type={data.get('task_type', '')}")
    print(f"total={len(answer_key)}")
    print(f"wrong={len(wrong)}")
    for key, user_answer, answer in wrong:
        print(f"{key}\tuser={user_answer}\tanswer={answer}")


if __name__ == "__main__":
    main()
