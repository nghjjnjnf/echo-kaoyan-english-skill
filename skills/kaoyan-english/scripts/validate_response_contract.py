#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


CONTRACTS = {
    "reading": [
        "题目陷阱分类",
        "相关原文截取",
        "中文参考翻译",
        "完整题目",
        "题干在问什么",
        "其他选项为什么错",
        "为什么选",
        "本题复盘",
    ],
    "cloze": [
        "空格陷阱分类",
        "相关原文截取",
        "中文参考翻译",
        "完整题目",
        "空格处需要什么",
        "其他选项为什么错",
        "为什么选",
        "本空复盘",
    ],
    "passage-translation": [
        "文章定位",
        "全文分段翻译",
        "重点词汇",
        "固定搭配与表达",
        "长难句与结构",
        "学习复盘",
    ],
    "writing": [
        "作文评分定位",
        "题目要求梳理",
        "分项评分",
        "逐句批改",
        "修改后版本",
        "修改建议",
        "下次可复用结构与知识点",
    ],
}


def main():
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Validate whether a generated response contains required rubric headings.")
    parser.add_argument("response_file")
    parser.add_argument("--type", choices=sorted(CONTRACTS), required=True)
    args = parser.parse_args()

    text = Path(args.response_file).read_text(encoding="utf-8")
    missing = [heading for heading in CONTRACTS[args.type] if heading not in text]
    if missing:
        for heading in missing:
            print(f"ERROR: missing heading: {heading}", file=sys.stderr)
        raise SystemExit(1)
    if args.type == "reading" and "定位原文" in text and "相关原文截取" not in text:
        print("ERROR: reading responses must use heading 相关原文截取, not 定位原文", file=sys.stderr)
        raise SystemExit(1)
    if "```" in text:
        print("ERROR: explanation responses must use paragraphs, blockquotes, or lists instead of fenced code blocks", file=sys.stderr)
        raise SystemExit(1)
    print("Response contract validation passed.")


if __name__ == "__main__":
    main()
