# 安装指南

本文只维护当前优先支持的路径：Codex、Claude Code 和 CodeBuddy / WorkBuddy。本项目会优先保证这些路径稳定。

## Codex

推荐使用 Codex 的 Skill Installer。安装后，Codex 会把 skill 复制到本机 Codex skill 目录并自动发现。

```text
$skill-installer install https://github.com/nghjjnjnf/echo-kaoyan-english-skill/tree/main/skills/kaoyan-english
```

安装完成后重启 Codex，然后可以用下面的问题测试触发：

```text
讲解 2025 年英一阅读 Text 1 第 21 题。
```

如果你是从 GitHub 克隆仓库进行本地开发，可以手动复制：

Windows PowerShell：

```powershell
git clone https://github.com/nghjjnjnf/echo-kaoyan-english-skill.git
cd echo-kaoyan-english-skill
python .\scripts\install_codex_skill.py
```

macOS 或 Linux：

```bash
git clone https://github.com/nghjjnjnf/echo-kaoyan-english-skill.git
cd echo-kaoyan-english-skill
python3 ./scripts/install_codex_skill.py
```

Codex 入口文件：

- `.codex-plugin/plugin.json`
- `skills/kaoyan-english/SKILL.md`
- `skills/kaoyan-english/agents/openai.yaml`
- `scripts/install_codex_skill.py`

本地开发提交前建议运行：

```powershell
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python skills\kaoyan-english\scripts\audit_corpus.py --skill skills\kaoyan-english
```

## Claude Code

Claude Code 有两种推荐用法。

### 方式一：项目级使用

适合你只想在这个仓库里使用 Echo_考研英语SKILL。

```bash
git clone https://github.com/nghjjnjnf/echo-kaoyan-english-skill.git
cd echo-kaoyan-english-skill
claude
```

启动后可以直接问：

```text
讲解 2025 年英二阅读 Text 2。
```

项目级入口文件：

- `CLAUDE.md`
- `.claude/skills/kaoyan-english/SKILL.md`
- `skills/kaoyan-english/SKILL.md`

其中 `.claude/skills/kaoyan-english/SKILL.md` 是 Claude Code wrapper，实际规则仍指向 `skills/kaoyan-english/SKILL.md`。

### 方式二：作为 Claude Code 插件安装

适合你希望在多个 Claude Code 项目里复用这个 skill。

在 Claude Code 里执行：

```text
/plugin marketplace add nghjjnjnf/echo-kaoyan-english-skill
/plugin install echo-kaoyan-english-skill@echo-kaoyan-english
/reload-plugins
```

插件模式下，skill 名称带插件命名空间，可直接调用：

```text
/echo-kaoyan-english-skill:kaoyan-english 讲解 2023 年英一阅读 Text 3 第 32 题。
```

Claude Code 插件入口文件：

- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`
- `skills/kaoyan-english/SKILL.md`

本地测试插件结构：

```bash
claude plugin validate
claude --plugin-dir .
```

如果 Claude Code 提示 marketplace 或 plugin 没有刷新，运行：

```text
/plugin marketplace update echo-kaoyan-english
/reload-plugins
```

## CodeBuddy / WorkBuddy

CodeBuddy / WorkBuddy 可按项目级 skill 使用。将仓库克隆到本地后，用 CodeBuddy / WorkBuddy 打开该目录即可：

```bash
git clone https://github.com/nghjjnjnf/echo-kaoyan-english-skill.git
cd echo-kaoyan-english-skill
```

项目级入口文件：

- `.codebuddy/skills/kaoyan-english/SKILL.md`
- `skills/kaoyan-english/SKILL.md`

`.codebuddy/skills/kaoyan-english/SKILL.md` 是兼容 wrapper，实际规则仍指向 `skills/kaoyan-english/SKILL.md`。启动后可以直接问：

```text
讲解 2025 年英一阅读 Text 1 第 21 题。
```

如果没有自动触发，尝试显式调用：

```text
使用 kaoyan-english skill，讲解 2025 年英一阅读 Text 1 第 21 题。
```

## 常见问题

### 安装后不触发怎么办

先用更明确的触发词，例如：

```text
使用 kaoyan-english skill，讲解 2024 年英一完形第 8 空。
```

然后检查：

- Codex 是否已经重启。
- Claude Code 是否执行了 `/reload-plugins`。
- CodeBuddy / WorkBuddy 是否是在仓库根目录打开，并且能读取 `.codebuddy/skills/kaoyan-english/SKILL.md`。
- 问题里是否包含考研英语、英一、英二、阅读、完形、翻译、作文、模拟题等明确语境。

### 能不能直接把整个仓库复制到 skill 目录

Codex 不建议这样做。Codex 应只安装 `skills/kaoyan-english/` 这个 skill 文件夹；仓库根目录的 README、GitHub Actions、Claude 插件配置和测试文件属于项目分发层，不属于单个 Codex skill。

### Claude Code 项目级和插件级有什么区别

项目级更适合开发和维护本仓库；插件级更适合把能力安装到其他项目里复用。插件级调用时会带命名空间，避免和其他 skill 重名。
