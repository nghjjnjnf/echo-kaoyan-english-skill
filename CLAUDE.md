@AGENTS.md

# Echo_考研英语SKILL For Claude Code

Claude Code should use this repository as a project-level teaching skill for 考研英语.

## Canonical Instructions

Read `skills/kaoyan-english/SKILL.md` first. It is the single source of truth for:

- intent recognition
- corpus lookup
- reading explanation format
- cloze explanation format
- translation scoring
- essay grading and model essay generation
- simulation generation

The Claude Code skill wrapper at `.claude/skills/kaoyan-english/SKILL.md` points back to the same canonical skill.

## Operating Rules

1. Resolve `english-i` or `english-ii`, year, section, and question number before answering.
2. Read `skills/kaoyan-english/references/index.json` first, then only the needed section files.
3. Preserve the required answer formats from the rubric files under `skills/kaoyan-english/references/rubrics/`.
4. Clearly label Echo-generated translation references and difficulty notes as non-official.
5. Do not add private data, local paths, or temporary source files to the repository.

## Broad Request Policy

Do not turn broad past-paper requests into short generic answers. If the user asks "解析 2021 年阅读理解", "讲一下 2023 年英一完形", "2024 年英语二阅读怎么做", or similar, use the canonical skill router and the relevant rubric.

- If English I vs English II is missing and both exist for the requested year, ask only for the track.
- If the track, year, and task type are known, start the structured response immediately.
- For broad reading, show the answer table for the requested scope, then begin with Reading Text 1 or the first requested text, with at most five questions per response in the full reading format.
- For broad cloze, show the 20-blank answer table, then explain blanks 1-5 in the full cloze format.
- Use short answers only when the user explicitly asks for answer-only, brief, or overview output.
