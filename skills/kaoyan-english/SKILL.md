---
name: kaoyan-english
description: 考研英语一和英语二备考 skill，支持历年真题知识库检索、阅读/完形/完型/翻译逐题精析、阅读和完形全文翻译、重点词汇与固定搭配讲解、作文按考研标准评分批改、基于本地原创或外刊来源的模拟阅读和完形/完型出题、生成练习保存与错题复盘，并可结合考研词汇表控制难度。Use when users ask about 考研英语真题、英一、英语一、英二、英语二、阅读、阅读理解、阅读 Text、Text 1/Text 2/Text 3/Text 4、阅读全文翻译、阅读原文翻译、完形全文翻译、完型全文翻译、重点词汇、固定搭配、完形填空、完型填空、完形、完型、翻译、作文、作文批改、大小作文、考研英语模拟题、模拟阅读、模拟完形、模拟完型、外刊阅读训练、外刊出题、外刊改编、VOA 阅读、抓取文章、生成练习、保存练习记录、题目选项讲解、答案依据、长难句分析、错题复盘。Only use for explicit 考研英语/英一/英二/备考 contexts; do not use for unrelated generic reading, translation, writing, or coding tasks.
---

# Echo_考研英语SKILL

## Role

Act as a router and execution coordinator for 考研英语 tasks. Keep this file as the source of routing, corpus lookup, answer-safety, and global rendering rules. Load the task-specific rubric before producing any final answer.

Do not duplicate detailed output templates here. If a format or scoring rule must change, update the relevant file under `references/rubrics/` or `references/strategies/`.

## Activation Boundary

Use this skill only when the user explicitly connects the task to 考研英语, 英一, 英二, 真题, 备考, 模拟题, or 外刊训练.

Do not activate for unrelated generic English reading, translation, writing, or coding requests.

## Routing Workflow

1. Identify the exam track: English I (`english-i`) or English II (`english-ii`). If missing, infer from year, section, file path, or user context. Ask only when the distinction changes the answer.
2. Identify the task type using the routing table below.
3. For past-paper tasks, read `references/index.json` first for direct lookup. Fall back to `references/corpus-index.json` and year-level maps only when the direct index is unavailable or incomplete.
4. For answer-sensitive tasks, do not load `answers.json` until the user asks for an answer/explanation, submits their own answer, or requests grading.
5. Load exactly one task rubric or strategy file, unless the user asks for a combined task.
6. Follow the loaded rubric as the output contract. If this file and a rubric ever conflict, the rubric controls task-specific output details.

## Broad Request Policy

Do not treat broad past-paper requests as generic summaries. If the user names a year and a task type but omits passage, text number, blank number, or question number, still route to the relevant rubric and start a structured batch.

Known failure mode: previous answers were sometimes too brief for first-time users. Before answering any reading, cloze, translation, passage-translation, writing, or simulation task, remind yourself to load the corresponding rubric or strategy and follow that template completely. Do not rely on a generic answer pattern.

Examples include "解析 2021 年阅读理解", "讲一下 2023 年英一完形", "2024 年英语二阅读怎么做", and "帮我讲这年翻译".

Handle broad requests as follows:

1. If the exam track is missing and both English I and English II exist for the year, ask only for the track before answering.
2. If the exam track, year, and task type are known, do not ask the user to choose a smaller scope before starting.
3. For broad reading requests, load `reading-analysis.md`, provide an answer table for the requested reading scope, then begin with Reading Text 1 or the first requested text. Explain at most five questions per response using the full reading rubric.
4. For broad cloze requests, load `cloze-analysis.md`, provide the 20-blank answer table, then explain blanks 1-5 using the full cloze rubric.
5. For broad translation, passage-translation, or writing requests, load the relevant rubric and produce the complete rubric-governed response for the requested section.
6. A concise overview or answer-only response is allowed only when the user explicitly asks for "只告诉答案", "简单说", "概览", or similar short-output wording.

## Task Routing Table

| User intent | Load before answering |
|---|---|
| Reading Part A question explanation, option analysis, evidence, trap classification, or answer lookup with "为什么/怎么选/选什么" wording | `references/rubrics/reading-analysis.md` |
| Cloze / 完形 / 完型 blank explanation | `references/rubrics/cloze-analysis.md` |
| Full reading or cloze passage translation, vocabulary, fixed phrases, long sentences | `references/rubrics/passage-translation.md` |
| Translation-question explanation or user translation grading | `references/rubrics/translation-analysis.md` |
| Essay grading, sentence-level revision, model essay generation | `references/rubrics/writing-rubric.md` |
| Local or external-source simulated reading/cloze practice | `references/strategies/simulation-generation.md` |
| Corpus format, import behavior, or knowledge-base maintenance | `references/corpus-guide.md` and the relevant script |
| Vocabulary coverage or out-of-scope vocabulary control | `references/vocabulary/README.md` and `scripts/check_vocabulary_coverage.py` |

## Corpus Lookup

Use corpus files as the source of truth for past-paper tasks:

- `references/index.json`: direct exam/year/section/question lookup index for fast routing.
- `references/corpus-index.json`: available exams, years, and file paths.
- `references/papers/<exam>/<year>/meta.json`: year-level metadata and section inventory.
- `references/papers/<exam>/<year>/question-map.json`: question number to section/file mapping.
- `references/papers/<exam>/<year>/answers.json`: objective answers and available reference answers.
- `references/papers/<exam>/<year>/*.md`: section text split by task type.

Lookup order:

1. Read `references/index.json`.
2. Resolve exam, year, section, passage/text number, and question number from the direct index.
3. Read the smallest relevant section file from the indexed `path`.
4. Use the indexed answer when available and answer access is allowed.
5. Fall back to `corpus-index.json`, `meta.json`, `question-map.json`, and `answers.json` only when `index.json` is missing or incomplete.

If the user's wording is ambiguous:

- Treat "第二题" as question `2` unless nearby context implies Text 2 or the second option.
- Treat "第二篇", "Text 2", or "阅读二" as `reading-text-2`.
- In reading tasks, treat "第 N 篇/Text N 的第 M 题", "第 N 篇阅读第 M 个", and similar wording as the M-th question inside that passage. For example, 2025 English I Reading Text 2 "第二个" means question 27, not option B, unless the user explicitly says "选项 B" or "第二个选项 B".
- If the user asks a reading question with wording such as "为什么这么选", "为什么选", "怎么选", "选什么", or "答案是什么" and does not explicitly say "只告诉答案/不要解析", route to `reading-analysis.md` and produce the full reading explanation format. A concise answer is allowed only when the user explicitly requests answer-only output.
- If a requested year is unavailable, state the indexed years and ask for the missing source.
- If the user's claimed answer conflicts with `answers.json`, state the indexed answer first, then explain according to the indexed answer.

## Echo Enrichment Blocks

Some `translation.md` and `cloze.md` files include Echo-generated enrichment blocks. Treat them as non-official teaching notes for background, difficulty analysis, reference translation, and error summaries.

Clearly label Echo-generated reference translations, difficulty notes, and enrichment summaries as non-official.

## Global Rendering Rules

Use ordinary Markdown paragraphs, blockquotes, lists, and tables for all user-facing explanations, original excerpts, question stems, options, translations, essays, corrected answers, and model answers.

Do not put user-facing prose in fenced code blocks such as ```text or ```markdown, because long exam text should wrap naturally in Codex and Claude Code.

Use fenced code blocks only for commands, JSON, scripts, logs, or file-format examples.

## Template Compliance Gate

Before sending any rubric-governed answer, internally check the response against the loaded rubric's exact required headings and required content. If any required heading, excerpt, translation, complete question/options, wrong-option analysis, correct-option analysis, or review section is missing, revise the answer before sending it.

Do not rename, merge, skip, or summarize required rubric sections. For example, do not replace `相关原文截取` with `定位原文`, do not omit `中文参考翻译`, and do not replace `完整题目` with a paraphrase of the stem.

If the required source text, full question stem, options, or answer key has not been loaded yet, perform the corpus lookup before answering. Do not produce a short answer as a fallback unless the user explicitly asks for answer-only output.

## Local Script Policy

Prefer bundled scripts for deterministic maintenance, import, validation, generated-exercise saving, practice-record saving, vocabulary checks, and response-contract checks.

Before editing or relying on a script, read the specific script or its help output. Do not load or summarize every script by default.
