---
description: Use for 考研英语真题、英一、英二、阅读、阅读理解、阅读 Text、完形、完型、翻译、作文批改、考研英语模拟题、模拟阅读、模拟完形、模拟完型、外刊出题、外刊改编、VOA 阅读、抓取文章、生成练习、保存练习记录、答案依据和错题复盘。
globs:
alwaysApply: false
---

# Echo_考研英语SKILL

Use `skills/kaoyan-english/SKILL.md` as the canonical instruction file.

When answering user questions:

1. Identify the exam track, year, section, and question number.
2. Read `skills/kaoyan-english/references/corpus-index.json` before opening paper files.
3. Load only the required files under `skills/kaoyan-english/references/papers/`.
4. Follow the task-specific rubric under `skills/kaoyan-english/references/rubrics/`.
5. Keep reading, cloze, translation, writing, and simulation formats separate.
6. Label Echo-generated translation references and enrichment notes as non-official.
7. Do not route unrelated generic reading, translation, writing, or coding tasks here unless the user explicitly connects the task to 考研英语, 英一, 英二, 真题, 备考, 模拟题, or 外刊训练.

Do not add raw Word/PDF files or third-party course materials to the public repository.
