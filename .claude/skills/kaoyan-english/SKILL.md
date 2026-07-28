---
name: kaoyan-english
description: 考研英语一和英语二备考 skill，支持历年真题知识库检索、阅读/阅读理解/完形/完型/翻译逐题精析、阅读和完形全文翻译、重点词汇与固定搭配讲解、作文评分批改、模拟阅读、模拟完形/完型、外刊出题、生成练习、保存练习记录和错题复盘。Use when users ask about 考研英语真题、英一、英语一、英二、英语二、阅读、阅读理解、阅读 Text、阅读全文翻译、阅读原文翻译、完形全文翻译、完型全文翻译、重点词汇、固定搭配、完形填空、完型填空、完形、完型、翻译、作文批改、考研英语模拟题、模拟阅读、模拟完形、模拟完型、外刊阅读训练、外刊出题、外刊改编、VOA 阅读、抓取文章、生成练习、保存练习记录、题目选项讲解、答案依据、长难句分析、错题复盘。Only use for explicit 考研英语/英一/英二/备考 contexts; do not use for unrelated generic reading, translation, writing, or coding tasks.
---

# Echo_考研英语SKILL Claude Code Wrapper

This is a Claude Code compatibility wrapper.

Use the canonical skill instructions at:

```text
../../../skills/kaoyan-english/SKILL.md
```

Then load only the needed references under:

```text
../../../skills/kaoyan-english/references/
```

Do not duplicate or reinterpret the full rubric here. The canonical skill and its bundled references define the required behavior.

Do not route unrelated generic reading, translation, writing, or coding tasks to this wrapper unless the user explicitly connects the task to 考研英语, 英一, 英二, 真题, 备考, 模拟题, or 外刊训练.

When a past-paper request is broad, such as "解析 2021 年阅读理解" or "讲一下 2023 年英一完形", do not give a short generic summary. Read the canonical skill, resolve the exam track/year/task, load the relevant rubric, and start the required batch response. Ask only for English I vs English II when that distinction is missing and affects the answer.

Known failure mode: previous answers were sometimes too brief for first-time users. Before answering, load the task-specific rubric or strategy and follow that template completely; do not rely on a generic explanation pattern.
