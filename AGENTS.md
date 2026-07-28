# Echo_考研英语SKILL Agent Guide

This repository is designed to be usable by Codex and Claude Code.

## Source Of Truth

Use `skills/kaoyan-english/SKILL.md` as the canonical skill instructions. Other agent entry files are compatibility wrappers and should not redefine the full behavior.

When working on the skill itself, update the canonical skill first, then update wrappers only when paths, supported tools, or usage instructions change.

## Agent Routing

Use this project when the user asks about:

- 考研英语真题、考研英语一/英语二真题
- 阅读、阅读理解、阅读 Text 逐题讲解、选项陷阱、定位句证据链
- 完形填空、完型填空、完形、完型空格讲解、搭配、语义和篇章逻辑
- 阅读/完形/完型全文翻译、重点词汇、固定搭配和长难句理解
- 翻译题解析、用户译文评分和修改
- 作文批改、作文评分、逐句批改、范文生成
- 考研英语模拟题、模拟阅读、模拟完形、模拟完型、外刊阅读训练、外刊出题、外刊改编、VOA 阅读、抓取文章、生成练习、保存练习记录和错题复盘

Do not route unrelated generic reading, translation, writing, or coding tasks to this skill unless the user explicitly connects the task to 考研英语, 英一, 英二, 真题, 备考, 模拟题, or 外刊训练.

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
