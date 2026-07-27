# Simulation Generation

Use this when generating external-source-style practice reading or cloze tasks.

Reading task requirements:

- Passage length: normally 400-550 English words unless the user requests otherwise.
- Questions: 5 multiple-choice questions with A-D options.
- Question mix: detail, inference, main idea/title, attitude, word meaning/example/function.
- Answers: keep hidden during practice mode.
- Explanation: after the user answers, explain with passage location, paraphrase, and distractor analysis.

Cloze task requirements:

- Passage length: normally 250-350 English words.
- Blanks: 10 or 20 according to the user's training load.
- Options: A-D for each blank.
- Test points: collocation, cohesion, grammar, lexical nuance, discourse logic.

Vocabulary control:

1. If a vocabulary list exists in `references/vocabulary/`, use it as the preferred allowed vocabulary.
2. Replace out-of-scope words with clearer in-scope expressions when this does not damage the passage logic.
3. If a technical term must remain, gloss it briefly in Chinese after the passage.

Source handling:

- Prefer user-provided article text or summaries.
- If using web material, summarize and adapt; avoid reproducing long source passages verbatim.
