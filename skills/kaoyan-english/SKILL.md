---
name: kaoyan-english
description: 考研英语一和英语二备考 skill，支持历年真题知识库检索、阅读/完形/翻译逐题精析、作文按考研标准评分批改、基于外刊的模拟阅读和完形出题，并可结合考研词汇表控制难度。Use when users ask about 考研英语真题、英一/英二、阅读 Text、完形填空、翻译、作文批改、考研英语模拟题、外刊阅读训练、题目选项讲解、答案依据、长难句分析、错题复盘。
---

# Echo_考研英语SKILL

## Core Workflow

1. Identify the exam track: English I (`english-i`) or English II (`english-ii`). If the user does not specify, infer from the requested year/resource path when possible; otherwise ask only when the distinction changes the answer.
2. Identify the task type: past-paper lookup, cloze explanation, reading explanation, translation explanation, essay grading, or simulation generation.
3. For past-paper tasks, read `references/corpus-index.json` first, then load only the requested year/section file from `references/papers/`.
4. For answer-sensitive tasks, avoid loading `answers.json` until the user asks for an answer/explanation or submits their own answer.
5. For generated practice, read `references/strategies/simulation-generation.md` and use `references/vocabulary/` if the user provides a vocabulary list.

## Past Paper Knowledge Base

Use the corpus files as the source of truth:

- `references/corpus-index.json`: available exams, years, and file paths.
- `references/papers/<exam>/<year>/meta.json`: year-level metadata and section inventory.
- `references/papers/<exam>/<year>/question-map.json`: question number to section/file mapping.
- `references/papers/<exam>/<year>/answers.json`: official/reference answers.
- `references/papers/<exam>/<year>/*.md`: section text split by task type.
- `translation.md` and `cloze.md` may include an `Echo` enrichment block at the bottom with non-official reference translations, whole-passage difficulty notes, and error summaries.

When the user asks a vague question such as "2015 第二题为什么选 B", resolve it as follows:

1. Treat "第二题" as question `2` unless nearby context implies Text 2 or the second option.
2. If the user says "第二篇", "Text 2", or "阅读二", map to `reading-text-2`.
3. If the requested year is unavailable, say which years are currently indexed and ask for the missing source file.
4. If the user's claimed answer conflicts with `answers.json`, state the indexed answer first, then explain the discrepancy.

## Explanation Standards

For reading questions, follow `references/rubrics/reading-analysis.md`.

Always include:

- question trap classification before the passage evidence, including question type judgment and the core trap pattern
- the smallest relevant original paragraph excerpt(s), quoted before analysis
- bold evidence inside the quoted excerpt with immediate labels such as `（定位句：...）` and `（辅助句：...）`
- a Chinese reference translation directly after the original excerpt, preserving the same evidence labels
- the complete question stem and all A-D options after the passage evidence and translation, with a concise Chinese translation immediately after each English stem/option line
- each distractor's error reason and trap type
- detailed answer logic tied to marked passage evidence after the distractor analysis
- synonym replacement between the correct option and the passage
- a practical review note for future questions

Use paragraph-rich explanations for reading questions. Avoid overly short, scattered comments. For multiple reading questions in one request, answer up to five questions in the same response while preserving the full single-question depth for each question. Split into batches only when the user asks for more than five reading questions.

For cloze questions, follow `references/rubrics/cloze-analysis.md`. Keep cloze explanations separate from reading explanations: cloze should focus on the blank position, local grammar, collocation, semantic fit, and discourse logic. When `cloze.md` contains an `Echo 完形整体难点评析与易错点总结` block, use it as background for final review, but still explain the requested blank(s) from the original sentence and options.

Always include:

- blank trap classification, including test point and core trap pattern
- the smallest useful local context around the blank, not the whole passage by default; always show the full sentence containing the blank without ellipses
- Chinese reference translation for the quoted context
- complete A-D options with Chinese translations; for cloze `完整题目`, arrange the four English options horizontally on one line and the four Chinese translations horizontally on the next line
- blank-level syntax, sentence role, and collocation
- discourse logic when the blank tests cohesion
- each distractor's error reason and cloze trap type
- detailed correct-option explanation after the distractor analysis
- final memory cue or method takeaway

For translation tasks, follow `references/rubrics/translation-analysis.md`. If the user provides their own translation, use translation grading mode; otherwise use translation explanation mode. Always identify whether the task is English I or English II before scoring, because English I uses five underlined segments for 10 points while English II uses one passage for 15 points. When `answers.json` does not include translation answers, read the `Echo 参考译文、难点评析与错误点总结` block in `translation.md` and clearly label it as a non-official Echo reference translation.

Always include:

- sentence skeleton
- clauses and modifiers
- key words in context
- literal draft translation
- polished Chinese translation
- likely scoring points

When grading a user's translation, always include:

- original English sentence, user translation, and reference translation
- track-specific score: English I segments are scored out of 2 points each; English II passage translation is scored out of 15 points total
- meaning-unit scoring table
- official-style deductions: for English I, major meaning mismatch caps that segment at 0.5; for English II, local mismatch loses the corresponding meaning-unit points and a whole-passage mismatch caps the total at 3/15; multiple submitted translations are graded as wrong if any one version is wrong; three or more Chinese typos deduct 0.5 by English I segment or from the English II passage total
- corrected version based on the user's translation
- targeted revision advice

## Essay Grading

For writing tasks, read `references/rubrics/writing-rubric.md`. Use writing grading mode when the user provides their own essay; use model essay mode when the user asks for 作文答案, 范文, 参考作文, or how to write a specific year's prompt.

Always identify the exam track and writing task before scoring or generating:

- English I small writing: 10 points.
- English I large writing: 20 points.
- English II small writing: 10 points.
- English II large writing: 15 points.
- If the user does not provide the original prompt, grade language and structure provisionally and mark task-completion scoring as provisional.

When grading a user's essay, return:

1. score and band
2. task requirement summary
3. dimension-level scoring diagnosis
4. sentence-level corrections
5. improved version based on the user's essay
6. revision advice
7. reusable structure and knowledge points

When generating a model essay, return:

1. task identification and prompt requirements
2. solid model essay (`扎实版经典范文`)
3. advanced model essay (`高级版经典范文`)
4. structure breakdown
5. reusable patterns, topic vocabulary, and self-writing checklist

## Simulation Generation

For external-source practice reading or cloze tasks:

1. Use a legitimate source summary or user-provided article text when available.
2. Do not reproduce long copyrighted source passages verbatim unless provided by the user for private processing.
3. Adapt the passage to 考研英语 difficulty and replace out-of-scope vocabulary with words from the user's 考研词汇 list when available.
4. Generate questions in the style of English I/II reading or cloze.
5. Keep answers hidden until the user submits responses or asks for the key.

## Scripts

- `scripts/import_docx_papers.py`: import a DOCX containing past papers into `references/papers/`, split by year and section, and build indexes.
- `scripts/search_papers.py`: quickly locate a year/section/question and print the relevant corpus paths and answer.
