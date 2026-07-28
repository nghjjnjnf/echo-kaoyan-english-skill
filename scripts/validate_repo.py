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


def validate_claude_plugin():
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    require(plugin_path.is_file(), "missing .claude-plugin/plugin.json")
    require(marketplace_path.is_file(), "missing .claude-plugin/marketplace.json")
    if not plugin_path.is_file() or not marketplace_path.is_file():
        return

    plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
    require(plugin.get("name") == "echo-kaoyan-english-skill", "Claude plugin name must be echo-kaoyan-english-skill")
    require(bool(re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", ""))), "Claude plugin version must use semantic versioning")
    require(bool(plugin.get("description")), "Claude plugin missing description")
    require(bool(plugin.get("author", {}).get("name")), "Claude plugin missing author name")

    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    require(marketplace.get("name") == "echo-kaoyan-english", "Claude marketplace name must be echo-kaoyan-english")
    require(bool(marketplace.get("owner", {}).get("name")), "Claude marketplace missing owner name")
    plugins = marketplace.get("plugins", [])
    require(isinstance(plugins, list) and len(plugins) == 1, "Claude marketplace must list exactly one plugin")
    if plugins:
        entry = plugins[0]
        require(entry.get("name") == plugin.get("name"), "Claude marketplace plugin name must match plugin.json")
        require(entry.get("source") == "./", "Claude marketplace plugin source must be ./")
        require(entry.get("version") == plugin.get("version"), "Claude marketplace plugin version must match plugin.json")


def validate_skill():
    path = SKILL / "SKILL.md"
    require(path.is_file(), "missing skills/kaoyan-english/SKILL.md")
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    require(text.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
    require(re.search(r"(?m)^name:\s*kaoyan-english\s*$", text), "SKILL.md name is incorrect")
    require(re.search(r"(?m)^description:\s*.+$", text), "SKILL.md missing description")
    require(len(text.splitlines()) <= 140, "SKILL.md should stay router-style; move task details to references")
    for drift_phrase in (
        "Always include:",
        "When grading a user's essay, return:",
        "When generating a model essay, return:",
    ):
        require(drift_phrase not in text, f"SKILL.md contains duplicated task-detail phrase: {drift_phrase}")
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


def validate_changelog():
    path = ROOT / "CHANGELOG.md"
    require(path.is_file(), "missing CHANGELOG.md")
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    require("## 2026-07-28" in text, "CHANGELOG.md missing current project cleanup entry")
    require("### Verified" in text, "CHANGELOG.md should record validation results")


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


def validate_client_entries():
    required_files = (
        "AGENTS.md",
        "CLAUDE.md",
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
        ".claude/skills/kaoyan-english/SKILL.md",
        "docs/INSTALLATION.md",
        "scripts/install_codex_skill.py",
    )
    for relative in required_files:
        require((ROOT / relative).is_file(), f"missing client entry file: {relative}")

    canonical = "skills/kaoyan-english/SKILL.md"
    for relative in (
        "AGENTS.md",
        "CLAUDE.md",
        "docs/INSTALLATION.md",
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
    ):
        path = ROOT / relative
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            missing = [term for term in trigger_terms if term not in text]
            require(not missing, f"{relative} missing trigger terms: {', '.join(missing)}")

    guard_phrase = "generic reading, translation, writing, or coding tasks"
    for relative in (
        "AGENTS.md",
        ".claude/skills/kaoyan-english/SKILL.md",
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


def main():
    validate_manifest()
    validate_claude_plugin()
    validate_skill()
    validate_json_files()
    validate_changelog()
    validate_public_data_boundary()
    validate_client_entries()
    if ERRORS:
        for error in ERRORS:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
