---
name: kaoyan-english
description: 考研英语一和英语二备考 skill，支持历年真题知识库检索、阅读/完形/完型/翻译逐题精析、阅读和完形全文翻译、重点词汇与固定搭配讲解、作文按考研标准评分批改、基于本地原创或外刊来源的模拟阅读和完形/完型出题、生成练习保存与错题复盘，并可结合考研词汇表控制难度。Use when users ask about 考研英语真题、英一、英语一、英二、英语二、阅读、阅读理解、阅读 Text、Text 1/Text 2/Text 3/Text 4、阅读全文翻译、阅读原文翻译、完形全文翻译、完型全文翻译、重点词汇、固定搭配、完形填空、完型填空、完形、完型、翻译、作文、作文批改、大小作文、考研英语模拟题、模拟阅读、模拟完形、模拟完型、外刊阅读训练、外刊出题、外刊改编、VOA 阅读、抓取文章、生成练习、保存练习记录、题目选项讲解、答案依据、长难句分析、错题复盘。Only use for explicit 考研英语/英一/英二/备考 contexts; do not use for unrelated generic reading, translation, writing, or coding tasks.
---

# Echo_考研英语SKILL

## Core Workflow

1. Identify the exam track: English I (`english-i`) or English II (`english-ii`). If the user does not specify, infer from the requested year/resource path when possible; otherwise ask only when the distinction changes the answer.
2. Identify the task type: past-paper lookup, cloze explanation, reading explanation, passage translation, translation-question explanation/grading, essay grading, or simulation generation.
3. For past-paper tasks, read `references/corpus-index.json` first, then load only the requested year/section file from `references/papers/`.
4. For answer-sensitive tasks, avoid loading `answers.json` until the user asks for an answer/explanation or submits their own answer.
5. For generated practice, read `references/strategies/simulation-generation.md` and use `references/vocabulary/` if the user provides a vocabulary list.
6. Do not activate for a general English reading, translation, writing, or coding request unless the user explicitly connects it to 考研英语, 英一, 英二, 真题, 备考, 模拟题, or 外刊训练.

## User-Facing Output Rendering

For all explanations, model essays, original excerpts, question stems, options, translations, and corrected answers, use ordinary Markdown paragraphs or blockquotes so text wraps naturally in Codex and other clients. Do not place user-facing prose in fenced code blocks such as ```text or ```markdown.

Use fenced code blocks only for actual commands, JSON, scripts, logs, or file-format examples. If a notice, essay, passage, question, or option list needs line breaks, use plain lines, blockquotes, or Markdown lists instead of code fences.

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

## Passage Translation

For reading or cloze full-passage translation tasks, read `references/rubrics/passage-translation.md`. Use this mode when the user asks to translate a reading passage, translate a cloze/完形 passage, show a complete Chinese translation, or explain key vocabulary and fixed expressions in the passage.

Do not confuse this with translation-question scoring. Passage translation is for comprehension support, not exam translation scoring.

Always include:

1. passage location
2. full paragraph-by-paragraph translation
3. key vocabulary in context
4. fixed phrases and collocations
5. long/difficult sentence notes
6. learning review

For cloze passages, keep blanks visible and do not reveal the answer key by default. If the user asks for a completed translation after requesting answers, then load `answers.json`, fill the blanks, and clearly label the output as answer-revealing.

## Essay Grading

For writing tasks, read `references/rubrics/writing-rubric.md`. Use writing grading mode when the user provides their own essay; use model essay mode when the user asks for 作文答案, 范文, 参考作文, or how to write a specific year's prompt.

Always identify the exam track and writing task before scoring or generating:

- English I small writing: 10 points.
- English I large writing: 20 points.
- English II small writing: 10 points.
- English II large writing: 15 points.
- Recommended length: English I small writing about 100 words; English I large writing 160-200 words; English II small writing about 100 words; English II large writing about 150 words.
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

1. Read `references/strategies/simulation-generation.md`.
2. Prefer local original generation by default when the user asks for 模拟阅读/模拟完形/外刊训练 without providing a URL or explicitly requesting a real source.
3. After local generation, briefly ask whether the user wants a future exercise adapted from a real external article. Do not fetch real articles by default.
4. If the user provides a URL or confirms they want a real article, first check fetch conditions: network/tool access, `scripts/fetch_source_article.py` availability, and whether the source domain is whitelisted. If any condition is missing, fall back to local original generation or ask the user to paste the article text.
5. Adapt any accepted source into an original 考研英语-style passage before writing questions. Avoid overly technical topics, dense terminology, and close paraphrase of copyrighted sources.
6. Generate reading or cloze questions in the style of English I/II.
7. Save a structured exercise draft with `scripts/save_exercise.py` when a durable local artifact is useful, then validate it with `scripts/validate_generated_exercise.py` before showing it.
8. In practice mode, show only the adapted passage and questions. Do not reveal the answer key or explanations until the user submits answers or asks for them.
9. When the user asks for answers, explain with the same reading/cloze evidence and distractor-analysis standards used for past-paper questions. For important examples, check the response headings with `scripts/validate_response_contract.py`.
10. If the user asks to record the practice after answering, save the adapted passage, questions, user answers, answer key, and explanation with `scripts/record_practice.py`. Use `scripts/list_practice_records.py` and `scripts/review_mistakes.py` for later错题复盘.

## Scripts

- `scripts/import_docx_papers.py`: import a DOCX containing past papers into `references/papers/`, split by year and section, and build indexes.
- `scripts/search_papers.py`: quickly locate a year/section/question and print the relevant corpus paths and answer.
- `scripts/fetch_source_article.py`: extract text from whitelisted external sources for simulation practice.
- `scripts/save_exercise.py`: save generated reading/cloze exercises with hidden answer keys before the user answers.
- `scripts/validate_generated_exercise.py`: verify generated exercise word count, question count, option completeness, and answer-key leakage.
- `scripts/check_vocabulary_coverage.py`: compare a generated passage with user-provided vocabulary lists and surface likely out-of-scope words.
- `scripts/audit_corpus.py`: audit corpus year folders, question maps, section files, and objective-answer coverage.
- `scripts/record_practice.py`: save local simulation practice records after the user answers.
- `scripts/list_practice_records.py`: list local practice-record JSON files.
- `scripts/review_mistakes.py`: summarize wrong answers from a saved practice record.
- `scripts/validate_response_contract.py`: check whether generated explanations include the required rubric headings.
