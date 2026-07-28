# Simulation Generation

Use this when generating external-source-style practice reading or cloze tasks.

## Source Selection

Prefer sources that are moderate in difficulty, education-friendly, and not packed with professional terminology.

| Priority | Source | Use mode | Notes |
|---|---|---|---|
| 1 | VOA Learning English | adaptable | Default source for readable news-style English. Check whether a page contains third-party wire material before reuse. |
| 2 | Simple English Wikipedia | adaptable with attribution | Good for background, science, culture, society, and general knowledge topics. Keep source attribution in metadata. |
| 3 | The Conversation | theme only | Use title, topic, and public facts for inspiration; write an original practice passage instead of rewriting the article. |
| 4 | BBC, NPR, Smithsonian, similar sources | theme only | Use only as topic inspiration and fact checking; do not reproduce or closely paraphrase full articles. |
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

1. Extract or read the source material.
2. Decide whether the source can be adapted or should be used only as topic inspiration.
3. Rewrite into an original 考研英语-style passage at the requested difficulty.
4. Control length and vocabulary.
5. Generate questions and hidden answer key.
6. Store the hidden answer key internally during the conversation until the user submits answers or asks for the key.

Reading task requirements:

- Passage length: normally 400-550 English words unless the user requests otherwise.
- Questions: 5 multiple-choice questions with A-D options.
- Question mix: detail, inference, main idea/title, attitude, word meaning/example/function.
- Questions should feel like 考研英语 Reading Part A: evidence-based, with plausible distractors and paraphrase rather than obvious word matching.
- Practice output: show the adapted passage and 5 questions only. Do not show answers, explanations, or answer-key hints.
- Answer mode: after the user submits answers or asks for the key, explain with original passage location, Chinese translation of key evidence, paraphrase/synonym replacement, and distractor analysis. Follow the reading-analysis rubric style.

Cloze task requirements:

- Passage length: normally 250-350 English words.
- Blanks: 10 or 20 according to the user's training load.
- Options: A-D for each blank.
- Test points: collocation, cohesion, grammar, lexical nuance, discourse logic.
- Practice output: show the adapted cloze passage and A-D options only. Do not show answers or explanations.
- Answer mode: after the user submits answers or asks for the key, explain blank by blank with local sentence context, grammar/collocation/discourse logic, and distractor analysis. Follow the cloze-analysis rubric style.

Vocabulary control:

1. If a vocabulary list exists in `references/vocabulary/`, use it as the preferred allowed vocabulary.
2. Replace out-of-scope words with clearer in-scope expressions when this does not damage the passage logic.
3. If a technical term must remain, gloss it briefly in Chinese after the passage.

Source handling:

- Prefer user-provided article text or summaries.
- If using web material, summarize and adapt; avoid reproducing long source passages verbatim.

## Practice Record Workflow

If the user asks to record, save, review later, or add the exercise to a local record:

1. Wait until the user has submitted answers and the explanation has been generated.
2. Save the adapted passage, questions, user answers, answer key, and explanation with `scripts/record_practice.py`.
3. Use the default local record directory unless the user names another path:
   - Windows: `%USERPROFILE%\.codex\kaoyan-english\practice-records`
   - macOS/Linux: `~/.codex/kaoyan-english/practice-records`
4. Tell the user the saved JSON and Markdown paths.
5. Do not commit practice records to the public repository.
