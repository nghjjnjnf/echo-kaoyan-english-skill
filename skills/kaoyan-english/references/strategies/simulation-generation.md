# Simulation Generation

Use this when generating local or external-source-style practice reading or cloze tasks.

Show generated passages, questions, options, and later explanations as ordinary Markdown paragraphs, blockquotes, or lists. Do not wrap practice passages or option lists in fenced code blocks, because long exam sentences should wrap naturally in Codex and other clients.

## Default Source Policy

Default to local original generation. When the user asks for 模拟阅读, 模拟完形, 模拟完型, 外刊阅读训练, or 外刊出题 without providing a URL or explicitly asking to fetch a real article, generate an original 考研英语-style passage first.

After giving the practice passage and questions, ask briefly whether the user wants the next exercise to be adapted from a real external article. Do not fetch a real article by default.

Fetch an external source only when one of these is true:

- the user provides a URL
- the user explicitly asks to 抓取/选取/改编 a real external article
- the user confirms after being asked

Before fetching, check all conditions:

1. The current client has network or browser access, or can run `scripts/fetch_source_article.py`.
2. The source domain is in the whitelist below.
3. The source mode allows adaptation, or the article will be used only as topic inspiration.

If any condition is missing, tell the user what is unavailable and continue with local original generation or ask the user to paste the article text.

## Source Selection

Prefer sources that are moderate in difficulty, education-friendly, and not packed with professional terminology.

| Priority | Source | Use mode | Notes |
|---|---|---|---|
| 1 | VOA Learning English | adaptable | Default source for readable news-style English. |
| 2 | Simple English Wikipedia | adaptable with attribution | Good for background, science, culture, society, and general knowledge topics. Keep source attribution in metadata. |
| 3 | The Conversation | theme only | Use title, topic, and public facts for inspiration; write an original practice passage instead of rewriting the article. |
| 4 | BBC, NPR, Smithsonian, similar sources | theme only | Use as topic inspiration and fact checking, then write a new practice passage. |
| Avoid | News in Levels, Breaking News English | restricted practice source | Useful for personal reading, but do not repackage their full learning materials as this skill's own exercise. |

When the user provides a URL, run `scripts/fetch_source_article.py <url>` when possible. If the script returns `source_mode=theme_only`, generate a new original passage based on the topic instead of adapting the article closely.

## Difficulty Filter

Before generating questions, check the source or topic:

- Prefer education, work, technology in daily life, health habits, environment, culture, society, family, and community topics.
- Avoid narrow medical, legal, financial, engineering, and academic-specialist topics unless the user explicitly requests them.
- Keep technical terms rare. Replace avoidable out-of-scope terms with clearer 考研-level expressions.
- If a term must remain for meaning, add a short Chinese gloss after the passage.
- Keep paragraphs coherent and exam-like; do not make the passage look like a list of facts.

## Adaptation Workflow

1. If no URL/article text is provided, generate a local original passage from the user's topic or a suitable broad topic.
2. If URL/article text is provided or confirmed, extract or read the source material.
3. Decide whether the source can be adapted or should be used only as topic inspiration.
4. Rewrite into an original 考研英语-style passage at the requested difficulty.
5. Control length and vocabulary. Reading passages must be 450-550 English words; cloze passages must be 300-350 English words. If the extracted source is outside the target range, compress, expand, or rewrite it into the required range before writing questions.
6. Create a question blueprint before writing options. The blueprint must include question/blank number, test point, intended answer, evidence, trap design, and difficulty level.
7. Ensure at least 30% of reading questions or cloze blanks are medium/hard. For 5 reading questions, at least 2 must be medium/hard. For 10 cloze blanks, at least 3 must be medium/hard. For 20 cloze blanks, at least 6 must be medium/hard.
8. Generate questions, a hidden answer key, a `difficulty_map`, and an evidence map that links each answer to sentence or paragraph evidence.
9. When the environment can run local scripts, save the structured exercise with `scripts/save_exercise.py` and validate it with `scripts/validate_generated_exercise.py` before showing it to the user.
10. Store the hidden answer key internally during the conversation until the user submits answers or asks for the key.

Reading task requirements:

- Passage length: normally 450-550 English words unless the user requests otherwise.
- Questions: 5 multiple-choice questions with A-D options.
- Question mix: detail, inference, main idea/title, attitude, word meaning/example/function.
- Difficulty mix: at least 2 of the 5 questions must be medium/hard. Medium/hard reading questions should require cross-sentence evidence, inference, attitude judgment, paragraph function, main idea/title judgment, or distractor elimination through scope/logic, not simple word matching.
- Questions should feel like 考研英语 Reading Part A: evidence-based, with plausible distractors and paraphrase rather than obvious word matching.
- Practice output: show the adapted passage and 5 questions only. Do not show answers, explanations, or answer-key hints.
- Answer mode: after the user submits answers or asks for the key, explain with original passage location, Chinese translation of key evidence, paraphrase/synonym replacement, and distractor analysis. Follow the reading-analysis rubric style.

Cloze task requirements:

- Passage length: normally 300-350 English words.
- Blanks: 10 or 20 according to the user's training load.
- Options: A-D for each blank.
- Test points: collocation, cohesion, grammar, lexical nuance, discourse logic.
- Difficulty mix: at least 30% of blanks must be medium/hard. A medium/hard blank should depend on broader context, contrast/cause/result logic, lexical recurrence, precise collocation, modifier scope, or a close distinction among same-part-of-speech options.
- Cloze type blueprint for a 10-blank training task: about 8 lexical-semantic blanks, 1-2 collocation/structure blanks, and about 1 discourse-logic blank. For a 20-blank task, scale this pattern while keeping a balanced answer-key distribution and plausible same-part-of-speech distractors.
- Practice output: show the adapted cloze passage and A-D options only. Do not show answers or explanations.
- Answer mode: after the user submits answers or asks for the key, explain blank by blank with local sentence context, grammar/collocation/discourse logic, and distractor analysis. Follow the cloze-analysis rubric style.

Vocabulary control:

1. If a vocabulary list exists in `references/vocabulary/`, use it as the preferred allowed vocabulary.
2. Replace out-of-scope words with clearer in-scope expressions when this does not damage the passage logic.
3. If a technical term must remain, gloss it briefly in Chinese after the passage.
4. When a user-provided vocabulary list is available as a file, run `scripts/check_vocabulary_coverage.py <passage-file> --vocab <vocab-file>` to identify likely out-of-scope words before finalizing the exercise.

Source handling:

- Prefer user-provided article text or summaries.
- If using web material, summarize and adapt; avoid reproducing long source passages verbatim.

## Practice Record Workflow

Generated exercise drafts and answered practice records are different:

- Exercise drafts are saved before the user answers. They contain passage, questions, hidden answer key, and evidence map.
- Practice records are saved after the user answers. They contain user answers, answer key, explanation, and correction history.

When a durable draft is useful before the user answers:

1. Save it with `scripts/save_exercise.py`.
2. Validate the saved JSON with `scripts/validate_generated_exercise.py`.
3. Show only the passage and questions to the user; do not show the answer key or evidence map.

If the user asks to record, save, review later, or add the exercise to a local record:

1. Wait until the user has submitted answers and the explanation has been generated.
2. Save the adapted passage, questions, user answers, answer key, and explanation with `scripts/record_practice.py`.
3. Use the default local record directory unless the user names another path:
   - Windows: `%USERPROFILE%\.codex\kaoyan-english\practice-records`
   - macOS/Linux: `~/.codex/kaoyan-english/practice-records`
4. Tell the user the saved JSON and Markdown paths.
5. Keep practice records local.

For later review:

- Use `scripts/list_practice_records.py` to find saved records.
- Use `scripts/review_mistakes.py <record-json>` to summarize wrong answers.
- Re-explain wrong questions with the reading/cloze rubric and include the original evidence again.

## Response Quality Checks

For important examples, documentation samples, or regression checks, save the generated answer as Markdown and run:

```bash
python scripts/validate_response_contract.py response.md --type reading
python scripts/validate_response_contract.py response.md --type cloze
```

This only checks required headings. It does not replace human review of evidence accuracy, option-trap analysis, or teaching quality.
