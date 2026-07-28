#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "kaoyan-english"
ERRORS = []


def require(condition, message):
    if not condition:
        ERRORS.append(message)


def validate_manifest():
    path = ROOT / ".codex-plugin" / "plugin.json"
    require(path.is_file(), "缺少 .codex-plugin/plugin.json")
    if not path.is_file():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("name") == "kaoyan-english", "plugin name 必须是 kaoyan-english")
    require(bool(re.fullmatch(r"\d+\.\d+\.\d+", data.get("version", ""))), "version 必须使用严格语义版本")
    require(data.get("skills") == "./skills/", "skills 路径必须是 ./skills/")
    require(data.get("license") == "MIT", "manifest 许可应为 MIT")
    interface = data.get("interface", {})
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        require(bool(interface.get(field)), f"manifest interface 缺少 {field}")


def validate_skill():
    path = SKILL / "SKILL.md"
    require(path.is_file(), "缺少 skills/kaoyan-english/SKILL.md")
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    require(text.startswith("---\n"), "SKILL.md 必须以 YAML frontmatter 开始")
    require(re.search(r"(?m)^name:\s*kaoyan-english\s*$", text), "SKILL.md name 不正确")
    require(re.search(r"(?m)^description:\s*.+$", text), "SKILL.md 缺少 description")
    require(len(text.splitlines()) <= 500, "SKILL.md 超过 500 行，应拆分到 references")
    for relative in (
        "references/rubrics/reading-analysis.md",
        "references/rubrics/cloze-analysis.md",
        "references/rubrics/translation-analysis.md",
        "references/rubrics/writing-rubric.md",
        "scripts/import_docx_papers.py",
        "scripts/search_papers.py",
    ):
        require((SKILL / relative).is_file(), f"缺少 {relative}")


def validate_json_files():
    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            ERRORS.append(f"无效 JSON: {path.relative_to(ROOT)}: {exc}")


def validate_public_data_boundary():
    forbidden = []
    invalid_answers = []
    invalid_meta = []
    invalid_paper_files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith("skills/kaoyan-english/assets/raw-papers/") and path.name != ".gitkeep":
            forbidden.append(relative)
        if relative.startswith("skills/kaoyan-english/references/papers/"):
            if path.name == ".gitkeep":
                continue
            if path.suffix not in {".md", ".json"}:
                invalid_paper_files.append(relative)
            if path.name == "answers.json":
                data = json.loads(path.read_text(encoding="utf-8"))
                answers = data.get("answers", {})
                for removed_section in ("translation", "writing"):
                    if removed_section in answers:
                        invalid_answers.append(f"{relative} contains {removed_section}")
            if path.name == "meta.json":
                data = json.loads(path.read_text(encoding="utf-8"))
                if "source_docx" in data:
                    invalid_meta.append(relative)
    require(not forbidden, "公开仓库包含应排除的数据文件: " + ", ".join(forbidden))
    require(not invalid_paper_files, "真题知识库包含不允许的文件类型: " + ", ".join(invalid_paper_files))
    require(not invalid_answers, "answers.json 不应包含翻译或作文答案: " + ", ".join(invalid_answers))
    require(not invalid_meta, "meta.json 不应包含本机原始 Word 路径: " + ", ".join(invalid_meta))


def main():
    validate_manifest()
    validate_skill()
    validate_json_files()
    validate_public_data_boundary()
    if ERRORS:
        for error in ERRORS:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
