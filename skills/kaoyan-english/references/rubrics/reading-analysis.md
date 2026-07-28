# Reading Analysis Rubric

Use this for 考研英语 Reading Comprehension Part A explanations.

## Required Behavior

When explaining a reading question, use an evidence-first, paragraph-rich style. Do not give short fragmented comments such as "A 错，原文没说". Each explanation paragraph should be substantial enough for a student to understand both the answer logic and the mistake pattern.

Treat common student wording such as "为什么这么选", "为什么选", "怎么选", "选什么", "答案是什么", "第二个为什么选", and "第几题选什么" as a request for this full reading-analysis format unless the user explicitly says "只告诉答案", "只要答案", "不用解析", or "不要展开". Do not downgrade these requests into a short answer plus brief evidence.

Use ordinary Markdown paragraphs or blockquotes for all user-facing excerpts, question text, options, translations, and explanations. Do not use fenced code blocks for passages, full questions, option lists, or model answer prose, because they do not wrap well in Codex.

1. Start with question trap classification. Identify exam track, year, text number, question number, official answer, question type, and the core trap pattern the question is testing.
2. Paste the smallest relevant original paragraph excerpt(s), not the whole passage.
3. Mark evidence directly inside the original excerpt. Bold the relevant sentence or phrase and add a Chinese parenthetical label immediately after it:
   - `**...**（定位句：...）` for the sentence that directly supports the answer.
   - `**...**（辅助句：...）` for sentences needed to understand contrast, cause, background, example, or conclusion.
   - `**...**（转折：...）` for contrast signals such as but, however, yet, although.
   - `**...**（因果：...）` for causal signals such as because, lead to, result in, explain.
4. Add a Chinese reference translation immediately after the original excerpt. Preserve the same evidence labels in Chinese, such as `（定位句）`, `（辅助句）`, `（转折）`, and `（因果）`, so lower-level students can check the meaning without re-parsing the English.
5. Display the complete question stem and all A-D options after the evidence excerpt and translation. Put a concise Chinese translation immediately after the English stem and after each English option. Do not abbreviate the stem with ellipses.
6. If a full paragraph is too long, excerpt the continuous part that contains the evidence plus enough before/after context. Do not force the student to compare against an unmarked paragraph.
7. Explain the question focus in Chinese before explaining options.
8. Explain the wrong options before explaining the correct option. For every wrong option, show its complete option text first, then what it says, why it fails, and the trap type.
9. Explain why the correct option is right through exact passage evidence and synonym replacement after the wrong-option analysis.
10. End with a practical review note for future questions.

## Output Format

Use exactly this structure.

## Professional Style Reference

Use the following as the professional style template for reading explanations. It is a style reference, not a replacement for the required section order above: keep `题目陷阱分类 -> 相关原文截取 -> 中文参考翻译 -> 完整题目 -> 题干在问什么 -> 其他选项为什么错 -> 为什么选 [Answer] -> 本题复盘`.

The answer should read like a teacher walking the student through the evidence chain:

- Begin with precise positioning: year, exam track, Text number, question number, indexed answer, question type, and core trap. Avoid vague openings such as "这题很简单".
- In `相关原文截取`, quote the decisive excerpt and mark it directly in the English: `**...**（定位句：...）`, `**...**（辅助句：...）`, `**...**（转折：...）`, or `**...**（因果：...）`. The label should explain why the sentence matters, not merely name it.
- In `题干在问什么`, explicitly separate what the question asks from what it does not ask. Use wording like: "它不是问……，而是问……". This prevents students from being pulled toward related but irrelevant passage details.
- For each wrong option, first show the complete option, then write one developed paragraph explaining the option's surface meaning, the exact mismatch with the passage, and the trap type. Do not write one-line comments.
- In `为什么选 [Answer]`, explain the correct option through exact synonym replacement and logical matching. Use compact mappings when helpful, such as `play the roles` 对应 `act him out`, then follow with a paragraph explaining why the match is complete.
- In `本题复盘`, give a transferable method: how to locate evidence, what phrase or relation was decisive, and what trap pattern to watch for next time.

Model phrasing pattern:

> 题干不是问“这个方法带来了什么效果”，也不是问“学生最后写了什么”，而是问这种方法本身要求学生做什么。题干关键词是 `...`，回到原文后，真正解释这个方法的句子是 `...`。所以答案必须体现“...”，而不能只抓住后文出现过的相关词。
>
> [Correct option] 的意思是“...”。它准确对应原文里的 `...`。这里的 `...` 不是泛泛含义，而是指“...”。后文的 `...` 又进一步确认这一点。同义替换关系很清楚：选项中的 `...` 对应原文中的 `...`；选项中的 `...` 对应原文中的 `...`。所以这个选项不是凭感觉选的，而是对原文核心动作/态度/因果关系的准确概括。
>
> [Wrong option] 看起来容易迷惑人，因为原文确实提到过 `...`。但题干问的是 `...`，原文强调的是 `...`，不是 `...`。这个选项把“...”偷换成了“...”。陷阱类型：偷换概念 / 主体错误 / 无中生有 / 干扰词复现。

### 题目陷阱分类

Include:

- 年份
- 科目
- 篇目
- 题号
- 正确答案
- 题型判断
- 核心陷阱

If the user claims a different answer from the indexed answer, state the indexed answer clearly and explain that the following analysis follows the indexed answer.

### 相关原文截取

Paste only the paragraph excerpt(s) needed to solve the question. Keep the original English. Bold the exact sentence or phrase that matters, and put the label in Chinese parentheses immediately after the bold part.

Example:

> ... **the exact evidence sentence**（定位句：直接支持正确答案） ...
> ... **however**（转折：提示前后意义变化） ...
> ... **background sentence**（辅助句：帮助理解题干背景） ...

For detail questions, usually quote one paragraph excerpt. For inference, attitude, main-idea, title, or structure questions, quote the minimum set of excerpts needed to support the answer. The displayed excerpt should be easy to scan: the student should be able to see the decisive evidence without comparing the explanation to the original passage again.

### 中文参考翻译

Translate the quoted excerpt into natural Chinese. Keep the same evidence labels after the corresponding Chinese sentence or phrase, so the student can match the English evidence to the Chinese meaning.

Use this format:

> ……**关键证据句的中文翻译**（定位句：直接支持正确答案）……
> ……**然而**（转折：提示前后意义变化）……
> ……**背景句的中文翻译**（辅助句：帮助理解题干背景）……

The translation should be accurate and readable. Do not over-explain grammar in this section; save analysis for later sections.

### 完整题目

Display the full question stem and all options exactly as they appear in the corpus. Do not omit words after `...` in the stem, and do not summarize options. Keep the English original first, then add the corresponding Chinese translation immediately after the stem and each option.

Use this format:

21. Full question stem...  
中文：完整题干中文翻译。

[A] Full option A.  
中文：A 选项中文翻译。

[B] Full option B.  
中文：B 选项中文翻译。

[C] Full option C.  
中文：C 选项中文翻译。

[D] Full option D.  
中文：D 选项中文翻译。

### 题干在问什么

Explain the real task of the question in Chinese after displaying the full question. Identify the key words in the question and explain how they point to the relevant paragraph or sentence. Clarify what the question is not asking if a common misunderstanding is likely.

### 其他选项为什么错

Explain the wrong options before the correct-option analysis. Do not write `已在上文解释` for the correct option here, because the correct option will be explained in the next section. For every wrong option, include:

- the complete option text
- the option's surface meaning
- why it fails against the passage evidence
- trap type

Use this format for each option:

A. [A] Full option text.  
分析：...  
陷阱类型：...

Each wrong-option explanation should be a complete paragraph, not a one-line dismissal. Never analyze an option without first showing its full original wording.

### 为什么选 [Answer]

Start by displaying the complete correct option text, then explain in one or more full paragraphs:

- the core meaning of the correct option
- the exact evidence from the bold `（定位句）` or `（辅助句）`
- the synonym replacement or logical match between the option and the passage
- why the answer is complete and not merely partially related

Use this mini-format when helpful:

- 选项中的 `...` 对应原文中的 `...`
- 选项中的 `...` 对应原文中的 `...`

### 本题复盘

Give a method takeaway. Mention how to locate evidence, how to compare options against the passage, and what trap pattern the student should watch for next time.

## Batch Reading Explanation Rule

When the user asks about multiple reading questions in one request, do not switch to a brief overview mode and do not answer only one question by default. Answer up to five reading questions in the same response, and apply the full single-question structure independently to every question:

1. `题目陷阱分类`
2. `相关原文截取`
3. `中文参考翻译`
4. `完整题目`
5. `题干在问什么`
6. `其他选项为什么错`
7. `为什么选 [Answer]`
8. `本题复盘`

For requests containing one to five reading questions, complete all requested questions in one response while preserving the full quality bar for each question. Do not reduce passage evidence, Chinese translation, complete question display, correct-option explanation, wrong-option explanation, or trap classification just because the request contains several questions.

If the user asks for more than five reading questions, split the response into batches of at most five questions. State which question numbers are covered in the current batch and continue with the next batch afterward if needed.

## Trap Types

Use these Chinese labels for wrong options:

- 无中生有: the option introduces information not stated or reasonably implied.
- 偷换概念: the option replaces the original subject, object, condition, scope, or action.
- 过度推断: the option goes beyond what the passage supports.
- 范围扩大: the option changes limited or conditional information into a broad or absolute claim.
- 范围缩小: the option removes an important part of the original meaning.
- 主体错误: the option attributes an action, opinion, or condition to the wrong person/group.
- 因果倒置: the option reverses cause and effect.
- 与原文相反: the option contradicts the passage.
- 答非所问: the option may be related or even true, but does not answer the question.
- 情感态度错判: the option misreads approval, criticism, neutrality, doubt, or concern.
- 干扰词复现: the option copies words from the passage but changes the meaning.

## Quality Bar

Prefer detailed, coherent paragraphs over many tiny bullets. Bullets are allowed for metadata and synonym replacement, but the reasoning itself should be explained in developed prose.
