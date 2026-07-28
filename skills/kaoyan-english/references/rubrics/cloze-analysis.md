# Cloze Analysis Rubric

Use this for Section I Use of English. Cloze explanations must use a different scheme from reading explanations. Do not force cloze questions into the reading format of paragraph evidence and reading option traps. Cloze is about the blank position, local grammar, collocation, semantic fit, and discourse logic.

If `cloze.md` contains an `Echo 完形整体难点评析与易错点总结` block, use that block as whole-passage background for topic, answer chain, and common error patterns. Do not replace blank-level analysis with the block; still locate and analyze the requested blank directly from the original cloze text.

## Required Behavior

When explaining a cloze blank, use a context-first, option-comparison style. Do not give short comments such as "A 搭配正确". Each explanation should show why the blank needs a specific word or phrase and why nearby alternatives fail.

1. Start with blank trap classification. Identify exam track, year, section, blank number, official answer, test point, and the core trap pattern.
2. Paste the smallest useful context, but always display the full sentence containing the blank without ellipses. Add the previous or next sentence only when needed for logic, reference, contrast, or cohesion; if included, display those sentences fully by default.
3. Mark the blank directly inside the excerpt as `**___ 5 ___**（空格：...）`. Bold the word or phrase that controls the answer and add labels such as `（搭配：...）`, `（语法：...）`, `（逻辑：...）`, `（指代：...）`, or `（复现：...）`.
4. Add a Chinese reference translation immediately after the excerpt. Preserve the same labels so lower-level students can understand what controls the blank.
5. Display the blank number and all A-D options after the context and translation. In the `完整题目` section, arrange the four English options horizontally on one line, then arrange the four corresponding Chinese translations horizontally on the next line.
6. Explain what the blank needs before analyzing options: part of speech, sentence role, controlled collocation, semantic direction, and discourse relation.
7. Explain the wrong options before explaining the correct option. For every wrong option, show its complete option text first, then what it means, why it fails, and the trap type.
8. Explain why the correct option fits through exact local context, collocation, grammar, and discourse logic after the wrong-option analysis.
9. End with a reusable memory cue or method takeaway.

## Output Format

Use exactly this structure.

### 空格陷阱分类

Include:

- 年份
- 科目
- 题型：完形填空 / Section I Use of English
- 空格号
- 正确答案
- 考点类型
- 核心陷阱

If the user claims a different answer from the indexed answer, state the indexed answer clearly and explain that the following analysis follows the indexed answer.

### 相关原文截取

Paste only the local context needed to solve the blank. The sentence containing the blank must be displayed in full and must not use `...` or ellipses, because its grammar and collocation are the evidence. Do not paste the whole passage unless the blank truly depends on the whole passage topic.

If the previous or next sentence is needed, display that sentence fully by default. Only omit a long unrelated inserted phrase when it is truly irrelevant to the blank, and state the omission clearly; do not omit words from the blank-containing clause itself.

Use this format:

```markdown
> Full previous sentence if needed.
> Full sentence with **___ 5 ___**（空格：需要判断...） and **key local clue**（搭配/语法/逻辑：...）.
> Full following sentence if needed.
```

### 中文参考翻译

Translate the quoted context into natural Chinese. Keep labels after the corresponding phrase.

Use this format:

```markdown
> 上一句中文，如果需要。
> 带有**第 5 空**（空格：需要判断...）和**关键线索**（搭配/语法/逻辑：...）的句子中文。
> 下一句中文，如果需要。
```

### 完整题目

Display the blank number and all options exactly as they appear in the corpus. For cloze only, show the four English options horizontally on one line, then show the corresponding Chinese translations horizontally on the next line. Keep the option letters aligned with their translations. Do not use the vertical one-option-per-line format in this section.

Use this format:

```text
5.
[A] Full option A.    [B] Full option B.    [C] Full option C.    [D] Full option D.
中文：[A] A 选项中文翻译。    [B] B 选项中文翻译。    [C] C 选项中文翻译。    [D] D 选项中文翻译。
```

### 空格处需要什么

Explain in Chinese:

- the part of speech needed by the blank
- the sentence role of the blank
- the word, phrase, or structure before/after the blank that controls the answer
- whether the logic is cause, result, contrast, concession, parallel, example, summary, or progression
- what meaning the completed sentence must express

This section is the core of cloze explanation. Prioritize context and collocation over isolated dictionary meanings.

### 其他选项为什么错

Explain the wrong options before the correct-option analysis. Do not write `已在上文解释` for the correct option here, because the correct option will be explained in the next section. For every wrong option, include:

- the complete option text
- the option's basic meaning
- why it fails against the blank's grammar, collocation, or logic
- trap type

Use this format for each option:

```markdown
A. `[A] Full option text.`
中文：...
分析：...
陷阱类型：...
```

Each wrong-option explanation should be a complete paragraph, not a one-line dismissal.

### 为什么选 [Answer]

Start by displaying the complete correct option text, then explain in one or more full paragraphs:

- how the option fits the needed part of speech and grammar
- how it forms a natural collocation with nearby words
- how it matches the local sentence meaning
- how it matches the broader discourse logic when relevant

Use this mini-format when helpful:

- 选项中的 `...` 与原文中的 `...` 构成搭配
- 选项中的 `...` 补足句子中的 `...` 成分
- 选项中的 `...` 呼应上文/下文的 `...`

### 本空复盘

Give a practical takeaway. Mention the controlling clue, the reusable collocation or logic pattern, and what trap the student should watch for in future cloze blanks.

## Batch Cloze Explanation Rule

When the user asks about multiple cloze blanks in one request, do not switch to a brief answer-key mode. Answer up to five blanks in the same response, and apply the full single-blank structure independently to every blank.

For requests containing one to five blanks, complete all requested blanks in one response while preserving the full quality bar for each blank. Do not reduce context, Chinese translation, option display, correct-option explanation, wrong-option explanation, or trap classification just because the request contains several blanks.

If the user asks for more than five blanks, give an answer table for all requested blanks first, then split detailed explanations into batches of at most five blanks.

## Cloze Trap Types

Use these Chinese labels for wrong options:

- 近义词混淆: the option has a similar dictionary meaning but does not fit the exact context.
- 搭配错误: the option does not naturally combine with the nearby word or phrase.
- 语法结构不匹配: the option does not fit the needed part of speech, clause pattern, or sentence role.
- 语义方向错误: the option has the wrong positive/negative, increase/decrease, active/passive, or abstract/concrete direction.
- 逻辑关系错误: the option breaks cause, result, contrast, concession, parallel, progression, or summary logic.
- 指代关系错误: the option misreads what a pronoun, noun phrase, or reference points to.
- 情感色彩不符: the option has the wrong tone, attitude, or evaluation.
- 原文复现误导: the option repeats a nearby word or topic but does not complete the blank correctly.
- 固定短语误判: the option looks plausible but does not form the required phrase.
- 只看中文误选: the option's Chinese meaning seems possible, but the English usage is wrong.

## Quality Bar

Prefer detailed, coherent paragraphs over scattered notes. A cloze explanation is successful when the student can see the exact clue that controls the blank and can explain why each distractor fails.
