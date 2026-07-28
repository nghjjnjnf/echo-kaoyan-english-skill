# Passage Translation Rubric

Use this when the user asks to translate a full reading passage, a full cloze passage, or a selected passage excerpt from 考研英语 materials. This is different from official translation-question scoring: do not score the user unless they explicitly submit their own translation for grading.

## Task Scope

Apply this mode when the user asks for:

- 阅读全文翻译
- 阅读 Text 全文翻译
- 完形全文翻译
- 完型全文翻译
- 把这篇文章翻译成中文
- 翻译并讲重点词汇
- 翻译并整理固定搭配

For reading passages, translate the requested passage or requested paragraphs. For cloze passages, keep blanks visible by default and translate the context naturally without revealing answers. If the user explicitly asks for a completed cloze translation after asking for answers, then use `answers.json` to fill blanks and clearly say it is an answer-revealing version.

## Required Behavior

1. Identify exam track, year, section, and passage range before translating.
2. Load only the requested `reading-text-*.md`, `cloze.md`, or user-provided passage.
3. Translate by paragraph, not by isolated sentence, so the Chinese preserves discourse flow.
4. Keep the original English paragraph immediately before its Chinese translation when the user needs comparison. If the passage is long, split into manageable paragraph pairs.
5. Bold important vocabulary and fixed phrases in the English paragraph only when they are discussed below; do not over-mark every difficult word.
6. Explain key vocabulary in context, including part of speech, contextual meaning, and a usable Chinese explanation.
7. Explain fixed phrases, collocations, and academic/exam-style expressions.
8. Include 2-4 long or difficult sentence notes when the passage contains them. Focus on sentence skeleton, modifier scope, reference, contrast, cause/result, concession, or abstract noun handling.
9. Use ordinary Markdown paragraphs or blockquotes. Do not use fenced code blocks for passages, translations, vocabulary, or explanations.
10. Do not include answer keys or option analysis unless the user asks for them.

## Output Format

Use exactly this structure.

### 文章定位

Include:

- 年份
- 科目
- 题型：阅读 / 完形 / 完型
- 篇目或范围
- 是否泄露答案：否 / 是
- 本次目标：全文理解 / 词汇积累 / 搭配积累 / 长难句理解

### 全文分段翻译

For each paragraph, use this format:

**Paragraph 1 原文**

> Original English paragraph. Bold only the words or phrases that will be explained later.

**Paragraph 1 译文**

中文自然译文。不要为了逐词对应牺牲中文通顺度，但不能漏掉否定、转折、因果、让步、比较、指代和修饰关系。

For cloze passages, keep blanks as `第 1 空` / `___ 1 ___` unless the user explicitly asks for answer-revealing translation.

### 重点词汇

Use a compact table:

| 词汇 | 词性 | 原文语境含义 | 常见含义 | 记忆/用法提示 |
|---|---|---|---|---|

Choose words that matter for comprehension or are common in 考研英语. Avoid filling the table with very basic words unless they have a special contextual meaning.

### 固定搭配与表达

Use a compact table:

| 搭配/表达 | 原文作用 | 中文含义 | 可复用例句或用法 |
|---|---|---|---|

Prioritize verb-noun collocations, adjective-noun collocations, preposition structures, discourse markers, and academic expressions.

### 长难句与结构

Select the most useful difficult sentences. For each one, include:

- 原句
- 句子主干
- 修饰成分/从句
- 翻译难点
- 推荐译法

If the passage is simple, say there are no major long sentences and instead explain 1-2 useful sentence patterns.

### 学习复盘

Summarize:

- 本文核心话题
- 本文最值得积累的 3-5 个表达
- 下次阅读类似文章时应注意的理解点
