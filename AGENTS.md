# Echo_考研英语SKILL Agent Guide

This repository is designed to be usable by Codex, Claude Code, and CodeBuddy / WorkBuddy project-level skills.

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

1. Read `skills/kaoyan-english/references/index.json` first for direct lookup.
2. Fall back to `skills/kaoyan-english/references/corpus-index.json` and year-level maps only when needed.
3. Load only the requested exam, year, and section from `skills/kaoyan-english/references/papers/`.
4. Use `question-map.json` to map question numbers to section files.
5. Use `answers.json` only when the user asks for answers or explanations.
6. For `translation.md` and `cloze.md`, treat `<!-- echo-enrichment:start -->` blocks as Echo-generated non-official teaching notes.

Do not load the whole corpus into context unless a repository maintenance task genuinely requires it.

## Broad Request Policy

Do not answer broad past-paper requests with a generic short summary. If the user says things like "解析 2021 年阅读理解", "讲一下 2023 年英一完形", or "2024 年英语二阅读怎么做", first resolve the exam track, year, and task type, then route to the canonical rubric.

Known failure mode: previous answers were sometimes too brief for first-time users. Before answering, load the task-specific rubric or strategy and follow that template completely; do not rely on a generic explanation pattern.

- If the exam track is missing and both English I and English II exist for that year, ask only for the track.
- If the exam track, year, and task type are known, start directly instead of asking the user to narrow the scope.
- Broad reading requests should show an answer table for the requested reading scope, then begin with Reading Text 1 or the first requested text, explaining at most five questions with the full `reading-analysis.md` format.
- Broad cloze requests should show the 20-blank answer table, then explain blanks 1-5 with the full `cloze-analysis.md` format.
- Do not produce an answer-only or overview-style response unless the user explicitly asks for "只告诉答案", "简单说", "概览", or similar short-output wording.

## Repository Data Boundary

The repository may include the maintained knowledge base, objective answers, and Echo-generated teaching notes. Do not add private data, local paths, or temporary source files.

## Validation

Before committing, run:

```powershell
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skills\kaoyan-english"
```
