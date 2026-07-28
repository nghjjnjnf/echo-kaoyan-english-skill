# 词汇资源

将考研词汇文件放在此目录。

建议采用 UTF-8 纯文本格式，每行一个单词：

```text
abandon
ability
able
...
```

模拟题工作流会优先使用这些文件控制阅读和完形材料的词汇范围，并在不破坏语义的前提下替换明显超纲词。

## 覆盖率检查

生成模拟阅读或完形后，可以先把文章保存为临时文本文件，再运行：

```bash
python scripts/check_vocabulary_coverage.py passage.txt --vocab skills/kaoyan-english/references/vocabulary/your-vocab.txt
```

脚本会输出：

- 总词数和不同单词数；
- 词表内/词表外不同单词数量；
- 覆盖率；
- 高频疑似超纲词。

使用结果时不要机械替换所有词。优先替换不影响语义的抽象词、低频形容词和专业名词；必须保留的术语应在题后给中文注释。
