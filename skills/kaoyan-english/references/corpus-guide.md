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

1. Read `corpus-index.json`.
2. Read the target year `meta.json`.
3. Read the smallest relevant section file.
4. Read `answers.json` only for grading, answer checking, or explanation.

Use stable IDs like `english-i-2014-reading-text-2-q26`.
