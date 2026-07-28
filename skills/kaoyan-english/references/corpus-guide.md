# Corpus Guide

Store past papers under `references/papers/<exam>/<year>/`.

Exam identifiers:

- `english-i`: 考研英语一
- `english-ii`: 考研英语二

Recommended files per year:

- `meta.json`: exam, year, sections, source file.
- `question-map.json`: maps question numbers to section files.
- `answers.json`: answer key and translation references.
- `cloze.md`: Section I Use of English.
- `reading-text-1.md` to `reading-text-4.md`: Section II Part A.
- `new-question-type.md`: Section II Part B.
- `translation.md`: Section II Part C.
- `writing.md`: Section III Writing.
- `paper.md`: cleaned full paper text for fallback lookup.

Lookup order:

1. Read `index.json` for direct `exam -> year -> section/question` lookup.
2. Read the smallest relevant section file from the indexed path.
3. Use indexed answers only for grading, answer checking, or explanation.
4. Fall back to `corpus-index.json`, target-year `meta.json`, `question-map.json`, and `answers.json` only when `index.json` is missing or incomplete.

Use stable IDs like `english-i-2014-reading-text-2-q26`.

Regenerate `index.json` after corpus changes:

```bash
python skills/kaoyan-english/scripts/build_index.py --skill skills/kaoyan-english
```
