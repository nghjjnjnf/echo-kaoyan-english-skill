# Echo_考研英语SKILL Agent Guide

This repository is designed to be usable by Codex, Claude Code, Cursor, Trae, and other coding agents that can read project instructions.

## Source Of Truth

Use `skills/kaoyan-english/SKILL.md` as the canonical skill instructions. Other agent entry files are compatibility wrappers and should not redefine the full behavior.

When working on the skill itself, update the canonical skill first, then update wrappers only when paths, supported tools, or usage instructions change.

## Agent Routing

Use this project when the user asks about:

- 考研英语一/英语二真题
- 阅读 Text 逐题讲解、选项陷阱、定位句证据链
- 完形填空空格讲解、搭配、语义和篇章逻辑
- 翻译题解析、用户译文评分和修改
- 作文评分、逐句批改、范文生成
- 外刊模拟阅读或完形训练

## Corpus Workflow

1. Read `skills/kaoyan-english/references/corpus-index.json` first.
2. Load only the requested exam, year, and section from `skills/kaoyan-english/references/papers/`.
3. Use `question-map.json` to map question numbers to section files.
4. Use `answers.json` only when the user asks for answers or explanations.
5. For `translation.md` and `cloze.md`, treat `<!-- echo-enrichment:start -->` blocks as Echo-generated non-official teaching notes.

Do not load the whole corpus into context unless a repository maintenance task genuinely requires it.

## Public Data Boundary

The repository may include the maintained public knowledge base, objective answers, and Echo-generated teaching notes. Do not add raw Word/PDF source files, third-party course notes, or unverified copyrighted material.

## Validation

Before committing, run:

```powershell
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skills\kaoyan-english"
```
