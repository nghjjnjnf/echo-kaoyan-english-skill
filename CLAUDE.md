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
2. Read `skills/kaoyan-english/references/corpus-index.json`, then only the needed section files.
3. Preserve the required answer formats from the rubric files under `skills/kaoyan-english/references/rubrics/`.
4. Clearly label Echo-generated translation references and difficulty notes as non-official.
5. Do not add raw Word/PDF papers or third-party materials to the public repository.
