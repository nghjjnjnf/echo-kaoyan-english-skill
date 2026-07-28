# Echo_考研英语SKILL

## Canonical Entry

Read `skills/kaoyan-english/SKILL.md` first. It defines the real behavior of the skill.

## Use Cases

- 考研英语真题与历年真题检索
- 阅读、阅读理解、阅读 Text 逐题精析
- 完形填空、完型填空、完形、完型空格讲解
- 翻译题解析与评分
- 作文批改、作文评分、批改和范文生成
- 考研英语模拟题、模拟阅读、模拟完形、模拟完型、外刊阅读训练、外刊出题、外刊改编、VOA 阅读、抓取文章、生成练习、保存练习记录和错题复盘

Do not route unrelated generic reading, translation, writing, or coding tasks to this skill unless the user explicitly connects the task to 考研英语, 英一, 英二, 真题, 备考, 模拟题, or 外刊训练.

## Corpus Rules

1. Start from `skills/kaoyan-english/references/corpus-index.json`.
2. Use `question-map.json` to locate question files.
3. Use `answers.json` only when answers are needed.
4. Read task rubrics from `skills/kaoyan-english/references/rubrics/`.
5. Treat Echo enrichment blocks as non-official teaching notes.

## Repository Safety

Do not commit raw Word/PDF files, unverified copyrighted content, or third-party course notes.
