# 真题数据指南

本项目随仓库发布基础真题知识库，同时保留用户本地导入流程。

基础知识库包含题面文本、题号映射、客观题答案、Echo 生成的翻译参考译文、翻译/完形整体难点评析与易错点总结。

## 已随仓库发布的数据

- 英语一：2010-2026 年。
- 英语二：2010-2026 年。
- 目录：`skills/kaoyan-english/references/papers/`。
- 快速索引：`skills/kaoyan-english/references/index.json`，用于按英一/英二、年份、题型和题号直接定位题型文件与答案。
- 年份索引：`skills/kaoyan-english/references/corpus-index.json`，用于记录可用年份、章节清单和回退检索。

## 支持的导入输入

当前导入器面向包含以下内容的 `.docx` 文件：

- 以 `2010英一`、`2010英二` 或标准考试标题标记年份。
- 使用 `Section I Use of English`、`Section II Reading Comprehension` 等英文段落标题。
- 阅读 Part A 使用 `Text 1` 至 `Text 4`。
- 同一年度试题后包含参考答案区。

不同来源的 Word 排版可能不同。导入后应抽查年份、题号和答案映射。

## 安装依赖

```bash
python -m pip install python-docx
```

## 导入英语一

```bash
python skills/kaoyan-english/scripts/import_docx_papers.py \
  "/path/to/english_i_part1.docx" \
  --exam english-i
```

## 导入英语二

```bash
python skills/kaoyan-english/scripts/import_docx_papers.py \
  "/path/to/english_ii_part1.docx" \
  --exam english-ii
```

可以连续导入多个文件。相同年份会按后一次导入结果更新，因此重复导入前应确认来源文件是否完整。

## 检查索引

查询某年某题：

```bash
python skills/kaoyan-english/scripts/build_index.py \
  --skill skills/kaoyan-english

python skills/kaoyan-english/scripts/search_papers.py \
  --exam english-i \
  --year 2025 \
  --question 21
```

预期输出包括年份目录、题型、对应 Markdown 文件和答案。

## 年份目录规范

```text
references/papers/<exam>/<year>/
├── meta.json
├── question-map.json
├── answers.json
├── paper.md
├── cloze.md
├── reading-text-1.md
├── reading-text-2.md
├── reading-text-3.md
├── reading-text-4.md
├── new-question-type.md
├── translation.md
└── writing.md
```

`exam` 只使用：

- `english-i`
- `english-ii`

## 必做抽查

每批导入后至少检查：

1. 运行 `build_index.py` 重新生成 `index.json`。
2. `index.json` 中是否能直接查到目标题号。
3. `corpus-index.json` 中是否出现正确年份。
4. `meta.json` 中题型文件是否完整。
5. `question-map.json` 是否将题号映射到正确篇目。
6. `answers.json` 是否将选择题答案放在正确题型下。
7. 阅读原文是否缺段，翻译下划线句是否完整。
8. 是否还残留页码、公众号、二维码说明或机构广告。

## 词汇表

可将考研词表放在 `references/vocabulary/`。建议使用 UTF-8 文本，每行一个词，文件名写清版本与来源。

## 数据安全

- 本地源文件默认被 `.gitignore` 排除。
- 提交前运行 `python scripts/validate_repo.py`，检查是否误加入本机路径、临时文件或作文答案。
- 若需要团队共享，请使用团队私有仓库或受控文件系统。
