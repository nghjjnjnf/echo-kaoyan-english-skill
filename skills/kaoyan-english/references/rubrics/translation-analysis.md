# Translation Analysis Rubric

Use this for Section II Part C translation.

## Task Modes

Choose the mode from the user's request:

- **Translation explanation mode**: use when the user asks how to translate a source sentence or asks for sentence analysis without providing their own translation.
- **Translation grading mode**: use when the user provides their own Chinese translation for a specific year/question and asks for scoring, correction, grading, 批改, 扣分, or 修改建议.

## Translation Explanation Mode

Output structure:

1. Original segment.
2. Sentence skeleton.
3. Clause breakdown.
4. Modifier handling.
5. Key words in context.
6. Literal translation.
7. Polished translation.
8. Scoring points and likely deductions.

Keep Chinese natural, but do not omit logical relations, negation, subjects, modifiers, or abstract nouns that carry meaning.

## Translation Grading Mode

Use this mode when the user submits a translation. Before scoring, identify the exam track because English I and English II use different translation formats and point totals.

- **English I (`english-i`)**: Section II Part C has five underlined segments, usually numbered 46-50, for 10 points total. Grade each segment on a 2-point scale. If the user submits one segment, score it out of 2. If the user submits multiple segments, grade each segment separately and give the total out of the corresponding subtotal or out of 10 for all five.
- **English II (`english-ii`)**: Section III Translation is one passage, usually question 46, for 15 points total. Grade the submitted passage out of 15. Split the passage into meaning units or sentence groups whose values total 15, not into 2-point English I segments.

### Required Behavior

1. Locate the original translation material from `references/papers/<exam>/<year>/translation.md`. Use the indexed reference answer from `answers.json` when available; otherwise use the `Echo 参考译文、难点评析与错误点总结` block appended to `translation.md` and label it as non-official.
2. Display the original English sentence or passage, the user's translation, and the reference translation before scoring.
3. Split scoring into meaning units. For English I, the meaning units for one segment must total 2 points. For English II, the meaning units for the whole passage must total 15 points.
4. Evaluate accuracy first, then fluency. Do not reward a fluent sentence that changes the original meaning.
5. Apply the official-style deduction rules:
   - English I: if a segment translation is clearly different from the original meaning, that segment score must not exceed 0.5 points.
   - English II: if one meaning unit is clearly different from the original meaning, score that unit very low or zero according to its value; if the whole passage is clearly unrelated to the original, the total score must not exceed 3/15.
   - If the user gives two or more translations for the same English I segment or the same English II passage and all are correct, score the correct translation. If any one provided version is wrong, grade according to the wrong version.
   - Count Chinese wrong characters/typos by scoring item. For English I, count per segment; three or more wrong characters in one segment deduct 0.5 points for that segment. For English II, count across the submitted passage; three or more wrong characters deduct 0.5 points from the total.
6. Explain deductions concretely: identify mistranslated words, missing subjects/objects, lost negation, wrong logical relation, wrong modifier scope, awkward but acceptable wording, and typo deductions.
7. Provide a corrected version based on the user's translation. Preserve the user's wording where it is acceptable, and revise only what is needed for accuracy and naturalness.
8. Provide short revision advice that tells the student what to fix next time.

### Output Format

Use exactly this structure.

### 翻译评分定位

Include:

- 年份
- 科目
- 题型形式：English I five underlined segments / English II one passage
- 题号或段落范围
- 满分
- 得分
- 评分结论

### 原句与译文

Use this format:

```markdown
原句/原文：...
用户译文：...
参考译文：...
```

If the user gives more than one translation for the same sentence, list every version and state that multiple-version scoring rules apply.
For English II, display the passage or the minimum complete passage portion needed to grade the user's submitted translation.

### 采分点拆解

Create a compact table:

| 采分点 | 分值 | 用户处理 | 得分 | 说明 |
|---|---:|---|---:|---|

For English I, the point values should total 2.0 for one segment. For English II, the point values should total 15.0 for the passage. Use increments such as 0.5, 0.25, 1, or another reasonable split when needed.

### 扣分细则适用

Apply these checks explicitly:

- 原意是否明显偏离：是/否；English I 明显偏离的单个小题最高 0.5 分；English II 局部偏离按采分点扣分，整段明显偏离最高 3/15。
- 是否提供多个译文：是/否；如果是，说明是否按错误译文给分。
- 错别字累计：English I 按每个小题累计，三个及以上扣 0.5 分；English II 按整段累计，三个及以上总分扣 0.5 分；否则不扣分。

### 修改后的译文

Give a polished corrected version based on the user's translation. For English I, correct the requested segment(s). For English II, correct the full passage or the submitted passage portion. Keep it close enough that the student can see how their version was repaired.

### 修改建议

Give focused advice. Mention:

- the most serious meaning error
- the grammar or structure that caused the deduction
- one reusable translation habit for future exams

## Scoring Guidance

Common deduction categories:

- 核心含义错误: main predicate, subject/object, or factual relation is wrong.
- 逻辑关系错误: cause, result, concession, contrast, condition, or negation is mistranslated.
- 修饰范围错误: modifiers attach to the wrong noun, verb, or clause.
- 漏译: an important meaning unit is omitted.
- 增译: unsupported information is added.
- 词义不准: a key word is translated with an inaccurate contextual meaning.
- 表达不通顺: Chinese is awkward but meaning remains mostly recoverable.
- 错别字扣分: three or more wrong Chinese characters in the sentence deduct 0.5 points.
