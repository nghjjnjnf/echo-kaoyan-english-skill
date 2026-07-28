# Writing Rubric

Use this for 考研英语 writing grading, revision, and model essay generation.

## Task Modes

Choose the mode from the user's request:

- **Writing grading mode**: use when the user provides their own essay and asks for scoring, 批改, 修改, 润色, 扣分原因, or 提分建议.
- **Model essay mode**: use when the user asks for 作文答案, 范文, 参考作文, 高分作文, or asks how to write a specific year's writing task.

Use ordinary Markdown paragraphs for all model essays, corrected essays, notices, letters, and revision prose. Do not wrap essays or notices in fenced code blocks. If a small-writing notice or letter needs line breaks, use plain lines with blank lines between parts so Codex can wrap long sentences naturally.

## Score Totals

Identify the exam track and writing task before scoring.

- **English I (`english-i`)**
  - Part A small writing: 10 points.
  - Part B large writing: 20 points.
  - Writing total: 30 points.
- **English II (`english-ii`)**
  - Part A small writing: 10 points.
  - Part B large writing: 15 points.
  - Writing total: 25 points.

If the user does not provide the original prompt, grade language and structure provisionally, but mark task-completion scoring as provisional.

## Recommended Length

Use these length targets when grading, revising, and generating model essays:

| Exam track | Task | Recommended length |
|---|---|---:|
| English I | Part A small writing | about 100 words |
| English I | Part B large writing | 160-200 words |
| English II | Part A small writing | about 100 words |
| English II | Part B large writing | about 150 words |

When grading a user's essay, treat length as part of task completion and communicative adequacy. Do not mechanically punish a small deviation, but flag answers that are obviously too short, too thin, or far beyond the expected scope. When generating a model essay, keep the model within the recommended range unless the user explicitly asks for a shorter outline or an expanded teaching version.

## Band Standards

Apply the same qualitative criteria across tasks, but map them to the correct point total.

| 档位 | 小作文 10 分 | 英一大作文 20 分 | 英二大作文 15 分 | 核心表现 |
|---|---:|---:|---:|---|
| 第五档 | 9-10 | 17-20 | 13-15 | 很好地完成任务；包含并有效阐述所有内容要点；语法和词汇准确、错误极少；衔接自然，层次清晰；格式和语体恰当；对目标读者完全产生预期效果。 |
| 第四档 | 7-8 | 13-16 | 10-12 | 较好地完成任务；包含所有要点但少数阐述不足；语法词汇基本准确，复杂结构偶有错误；衔接较自然，层次较清晰；格式语体基本恰当。 |
| 第三档 | 5-6 | 9-12 | 7-9 | 基本完成任务；遗漏部分内容但包含多数要点；存在一些语法或词汇错误但基本不影响理解；衔接简单，内容基本连贯；格式语体基本合理。 |
| 第二档 | 3-4 | 5-8 | 4-6 | 未能按要求完成任务；遗漏或无效表达较多，有无关内容；语法结构单调、词汇有限；错误较多并影响理解；衔接不足，格式或语体不当。 |
| 第一档 | 1-2 | 1-4 | 1-3 | 内容严重不足或偏题；语言错误频繁，读者难以理解；结构混乱；基本没有完成交际目的。 |
| 零分 | 0 | 0 | 0 | 空白、完全跑题、照抄无关内容，或几乎无法判断为有效英文作文。 |

## Dimension Scoring Guide

Use this as a quantitative aid before assigning the final band. The final score must still match the band descriptors above.

For a 10-point small writing task:

| Dimension | Points | What to check |
|---|---:|---|
| Task completion and content | 3 | Whether all required information, communicative purpose, recipient, and format are covered. |
| Organization and cohesion | 2 | Whether ideas are ordered naturally and connected with appropriate transitions. |
| Grammar and sentence control | 2 | Whether tense, agreement, clauses, articles, prepositions, and sentence boundaries are reliable. |
| Vocabulary and register | 2 | Whether word choice, collocation, tone, and politeness match the task. |
| Mechanics | 1 | Spelling, punctuation, capitalization, signature, and layout. |

For English I Part B large writing out of 20, scale the same dimensions as follows:

| Dimension | Points |
|---|---:|
| Task completion, picture/topic interpretation, and argument relevance | 6 |
| Content development and reasoning | 4 |
| Organization and paragraph logic | 3 |
| Grammar and sentence variety | 3 |
| Vocabulary range, collocation, and register | 3 |
| Mechanics | 1 |

For English II Part B large writing out of 15, scale the same dimensions as follows:

| Dimension | Points |
|---|---:|
| Task completion, chart/topic interpretation, and relevance | 5 |
| Content development and reasoning | 3 |
| Organization and paragraph logic | 2 |
| Grammar and sentence control | 2 |
| Vocabulary range, collocation, and register | 2 |
| Mechanics | 1 |

Deduction anchors:

- Severe task mismatch or missing required genre usually caps the answer at the third band even if some sentences are fluent.
- Mostly irrelevant content caps the answer at the second band.
- Several grammar errors that repeatedly block understanding cap the answer at the second or low third band.
- Template-like language that does not respond to the specific prompt should lose task-completion and content-development points.
- Word count that is clearly too short should reduce task completion and content development; excessive length should reduce organization and relevance when it creates repetition or off-task content.

## Writing Grading Mode

### Required Behavior

1. Locate the original prompt from `references/papers/<exam>/<year>/writing.md` when the user gives a year/task.
2. Identify whether the essay is small writing or large writing, and whether it belongs to English I or English II.
3. Score against the correct point total. Do not score English II large writing out of 20.
4. Evaluate these dimensions:
   - task completion and content relevance
   - coverage and development of required points
   - organization and paragraph logic
   - grammar accuracy and sentence control
   - vocabulary appropriateness and range
   - cohesion devices and transitions
   - register, format, punctuation, and spelling
   - reader effect / communicative success
5. Give sentence-level corrections in a compact table. Preserve the user's meaning when possible.
6. Provide an improved version based on the user's essay, not a completely unrelated model essay.
7. Extract reusable writing knowledge so the student can write better next time.

### Output Format

Use exactly this structure.

### 作文评分定位

Include:

- 年份/题目来源
- 科目：English I / English II
- 题型：小作文 / 大作文
- 满分
- 建议字数
- 实际字数
- 得分
- 档位
- 一句话诊断

### 题目要求梳理

Summarize what the prompt asks the student to do. For small writing, identify the required communicative purpose, recipient, and format. For large writing, identify the picture/chart/topic, core issue, and expected stance or analysis.

### 分项评分

Use this table:

| 维度 | 分值 | 得分 | 表现 | 扣分原因 | 建议 |
|---|---:|---:|---|---|---|

Cover task completion, content, organization, grammar, vocabulary, cohesion, and format/register.

### 逐句批改

Use this table:

| 原句 | 问题 | 修改 |
|---|---|---|

Focus on errors that affect score: grammar, collocation, unclear reference, Chinglish, spelling, punctuation, and format.

### 修改后版本

Rewrite the user's essay into a stronger exam-ready version. Keep the original intended meaning and task response when possible.

### 修改建议

Give focused advice:

- the top 2-3 score-limiting problems
- what to fix first
- one practical training method

### 下次可复用结构与知识点

Provide:

- paragraph structure
- useful sentence patterns
- topic vocabulary or functional phrases
- common mistakes to avoid

## Model Essay Mode

### Required Behavior

1. Locate the original writing prompt from `references/papers/<exam>/<year>/writing.md` when a year/task is specified.
2. Identify English I or English II and small writing or large writing.
3. If the user asks for one version, provide the requested style. If the user does not specify, provide both:
   - **扎实版经典范文**: clear structure, safe grammar, accurate vocabulary, easy for ordinary students to imitate.
   - **高级版经典范文**: richer expression, stronger cohesion, more varied sentence patterns, but still natural and exam-appropriate.
4. Do not produce empty template prose that could fit any topic. The essay must respond to the specific prompt content.
5. After the model essay, explain how it is built so the user can reproduce it independently.

### Output Format

Use exactly this structure.

### 作文任务定位

Include:

- 年份
- 科目：English I / English II
- 题型：小作文 / 大作文
- 满分
- 建议字数
- 写作任务

### 题目要求拆解

List the required content points and the expected structure.

### 扎实版经典范文

Write an exam-ready model answer with reliable language and moderate difficulty.

### 高级版经典范文

Write a stronger model answer with better diction, transitions, and sentence variety. Keep it realistic for exam writing.

### 结构梳理

Explain the paragraph-by-paragraph structure. For small writing, include salutation/body/closing/signature when relevant. For large writing, explain introduction, description/analysis, argument, and conclusion as needed.

### 可复用知识点

Provide reusable:

- opening patterns
- transition patterns
- argument patterns
- closing patterns
- topic words and collocations

### 自写提醒

Give a short checklist the student can use next time before submitting an essay.
