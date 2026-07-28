# 多 Agent 使用指南

Echo_考研英语SKILL 采用“一份核心规则，多种 Agent 入口”的结构。核心能力放在 `skills/kaoyan-english/SKILL.md`，不同工具只通过自己的项目规则文件引用它。

所有入口只应在明确的考研英语、英一、英二、真题、备考、模拟题或外刊训练语境下使用。普通英文阅读、翻译、写作或代码任务不要自动套用本 skill。

## Codex

Codex 的标准入口是：

- `.codex-plugin/plugin.json`
- `skills/kaoyan-english/SKILL.md`
- `skills/kaoyan-english/agents/openai.yaml`

安装方式：

```text
$skill-installer install https://github.com/nghjjnjnf/echo-kaoyan-english-skill/tree/main/skills/kaoyan-english
```

## Claude Code

Claude Code 的项目级入口是：

- `CLAUDE.md`
- `.claude/skills/kaoyan-english/SKILL.md`

使用方式：克隆仓库后在 Claude Code 中打开项目，让 Claude Code 读取项目说明。`.claude/skills/kaoyan-english/SKILL.md` 是兼容包装器，实际规则仍指向 `skills/kaoyan-english/SKILL.md`。

## Cursor

Cursor 的项目规则入口是：

- `AGENTS.md`
- `.cursor/rules/kaoyan-english.mdc`
- `.cursor/rules/kaoyan-english/RULE.md`

使用方式：在 Cursor 中打开仓库，Agent 处理考研英语相关问题时会读取项目规则，并按规则进入 `skills/kaoyan-english/SKILL.md` 与对应知识库文件。仓库同时保留 `.mdc` 文件和 `RULE.md` 目录版入口，以兼容不同版本和不同团队设置。

## Trae

Trae 的项目规则入口是：

- `.trae/project_rules.md`
- `.trae/rules/kaoyan-english.md`

使用方式：在 Trae 中打开仓库，先让 Agent 阅读 `.trae/project_rules.md`，再按其中路径进入核心 skill。

## 维护原则

- 只把完整行为写在 `skills/kaoyan-english/SKILL.md` 和 `references/` 中。
- 其他入口文件只写触发、路径和约束，不复制完整解析模板。
- 修改题型规则后，优先更新核心 skill 和 rubrics，再检查各工具入口是否仍然指向正确路径。
- 修改触发词后，运行 `python scripts/validate_repo.py` 检查 Codex、Claude Code、Cursor 和 Trae 入口是否同步。
- 提交前运行 `python scripts/validate_repo.py` 和单元测试。
