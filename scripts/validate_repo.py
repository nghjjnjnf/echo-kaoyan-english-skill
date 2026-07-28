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
    require(path.is_file(), "missing .codex-plugin/plugin.json")
    if not path.is_file():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("name") == "kaoyan-english", "plugin name must be kaoyan-english")
    require(bool(re.fullmatch(r"\d+\.\d+\.\d+", data.get("version", ""))), "version must use semantic versioning")
    require(data.get("skills") == "./skills/", "skills path must be ./skills/")
    require(data.get("license") == "Unlicense", "manifest license must be Unlicense")
    interface = data.get("interface", {})
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        require(bool(interface.get(field)), f"manifest interface missing {field}")


def validate_skill():
    path = SKILL / "SKILL.md"
    require(path.is_file(), "missing skills/kaoyan-english/SKILL.md")
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    require(text.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
    require(re.search(r"(?m)^name:\s*kaoyan-english\s*$", text), "SKILL.md name is incorrect")
    require(re.search(r"(?m)^description:\s*.+$", text), "SKILL.md missing description")
    require(len(text.splitlines()) <= 500, "SKILL.md exceeds 500 lines; move detail to references")
    for relative in (
        "references/rubrics/reading-analysis.md",
        "references/rubrics/cloze-analysis.md",
        "references/rubrics/translation-analysis.md",
        "references/rubrics/passage-translation.md",
        "references/rubrics/writing-rubric.md",
        "scripts/import_docx_papers.py",
        "scripts/search_papers.py",
        "scripts/fetch_source_article.py",
        "scripts/record_practice.py",
        "scripts/save_exercise.py",
        "scripts/validate_generated_exercise.py",
        "scripts/check_vocabulary_coverage.py",
        "scripts/audit_corpus.py",
        "scripts/list_practice_records.py",
        "scripts/review_mistakes.py",
        "scripts/validate_response_contract.py",
    ):
        require((SKILL / relative).is_file(), f"missing {relative}")


def validate_json_files():
    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            ERRORS.append(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")


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
                for removed_section in ("writing",):
                    if removed_section in answers:
                        invalid_answers.append(f"{relative} contains {removed_section}")
            if path.name == "meta.json":
                data = json.loads(path.read_text(encoding="utf-8"))
                if "source_docx" in data:
                    invalid_meta.append(relative)
    require(not forbidden, "public repo contains excluded raw data files: " + ", ".join(forbidden))
    require(not invalid_paper_files, "paper corpus contains unsupported file types: " + ", ".join(invalid_paper_files))
    require(not invalid_answers, "answers.json must not contain writing answers: " + ", ".join(invalid_answers))
    require(not invalid_meta, "meta.json must not contain local source_docx paths: " + ", ".join(invalid_meta))


def validate_agent_compatibility():
    required_files = (
        "AGENTS.md",
        "CLAUDE.md",
        ".claude/skills/kaoyan-english/SKILL.md",
        ".cursor/rules/kaoyan-english.mdc",
        ".cursor/rules/kaoyan-english/RULE.md",
        ".trae/project_rules.md",
        ".trae/rules/kaoyan-english.md",
        "docs/AGENT_COMPATIBILITY.md",
    )
    for relative in required_files:
        require((ROOT / relative).is_file(), f"missing agent compatibility file: {relative}")

    canonical = "skills/kaoyan-english/SKILL.md"
    for relative in (
        "AGENTS.md",
        "CLAUDE.md",
        ".cursor/rules/kaoyan-english.mdc",
        ".cursor/rules/kaoyan-english/RULE.md",
        ".trae/project_rules.md",
        ".trae/rules/kaoyan-english.md",
        "docs/AGENT_COMPATIBILITY.md",
    ):
        path = ROOT / relative
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            require(canonical in text, f"{relative} should point to {canonical}")

    trigger_terms = (
        "考研英语真题",
        "英一",
        "英二",
        "阅读",
        "完形",
        "完型",
        "翻译",
        "全文翻译",
        "重点词汇",
        "固定搭配",
        "作文批改",
        "模拟阅读",
        "模拟完形",
        "外刊出题",
        "抓取文章",
        "保存练习记录",
    )
    for relative in (
        "AGENTS.md",
        ".claude/skills/kaoyan-english/SKILL.md",
        ".cursor/rules/kaoyan-english.mdc",
        ".cursor/rules/kaoyan-english/RULE.md",
        ".trae/project_rules.md",
        ".trae/rules/kaoyan-english.md",
    ):
        path = ROOT / relative
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            missing = [term for term in trigger_terms if term not in text]
            require(not missing, f"{relative} missing trigger terms: {', '.join(missing)}")

    guard_phrase = "generic reading, translation, writing, or coding tasks"
    for relative in (
        "AGENTS.md",
        ".cursor/rules/kaoyan-english.mdc",
        ".cursor/rules/kaoyan-english/RULE.md",
        ".trae/project_rules.md",
        ".trae/rules/kaoyan-english.md",
    ):
        path = ROOT / relative
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            require(guard_phrase in text, f"{relative} missing non-kaoyan trigger guard")

    claude_skill = ROOT / ".claude" / "skills" / "kaoyan-english" / "SKILL.md"
    if claude_skill.is_file():
        text = claude_skill.read_text(encoding="utf-8")
        require(text.startswith("---\n"), "Claude skill wrapper must start with YAML frontmatter")
        require(re.search(r"(?m)^name:\s*kaoyan-english\s*$", text), "Claude skill wrapper name is incorrect")
        require("../../../skills/kaoyan-english/SKILL.md" in text, "Claude skill wrapper must link to the canonical skill")

    cursor_rule = ROOT / ".cursor" / "rules" / "kaoyan-english.mdc"
    if cursor_rule.is_file():
        text = cursor_rule.read_text(encoding="utf-8")
        require(text.startswith("---\n"), "Cursor rule must start with MDC frontmatter")
        require("description:" in text and "alwaysApply:" in text, "Cursor rule frontmatter is incomplete")

    cursor_rule_folder = ROOT / ".cursor" / "rules" / "kaoyan-english" / "RULE.md"
    if cursor_rule_folder.is_file():
        text = cursor_rule_folder.read_text(encoding="utf-8")
        require(text.startswith("---\n"), "Cursor RULE.md must start with frontmatter")
        require("description:" in text and "alwaysApply:" in text, "Cursor RULE.md frontmatter is incomplete")


def main():
    validate_manifest()
    validate_skill()
    validate_json_files()
    validate_public_data_boundary()
    validate_agent_compatibility()
    if ERRORS:
        for error in ERRORS:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
