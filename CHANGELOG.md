# 修改记录

本项目从 2026-07-28 起使用此文件记录每次对外可见的修改。后续提交应在提交前补充对应条目，说明做了什么、影响哪些客户端或功能、验证了什么。

## 2026-07-28

### Changed

- 将 `skills/kaoyan-english/SKILL.md` 重构为路由器式入口：主文件只保留触发边界、任务路由、知识库查找顺序、答案安全和全局渲染规则。
- 阅读、完形、全文翻译、翻译评分、作文和模拟题的具体输出要求统一交给对应 `references/rubrics/` 或 `references/strategies/` 文件，降低规则漂移和上下文浪费。
- `scripts/validate_repo.py` 增加 router-style 约束，防止主 `SKILL.md` 再次膨胀并重复题型细则。
- 将项目优先支持范围收敛为 Codex 和 Claude Code。
- README 改为只展示 Codex / Claude Code 的安装与客户端支持信息。
- `AGENTS.md` 项目定位更新为 Codex 和 Claude Code。
- `scripts/validate_repo.py` 改为校验 Codex / Claude Code 必需入口，并要求存在修改记录文件。
- `skills/kaoyan-english/agents/openai.yaml` 更新 Codex 展示文案。

### Added

- 新增 Claude Code 插件结构：`.claude-plugin/plugin.json` 与 `.claude-plugin/marketplace.json`。
- 新增统一安装指南：`docs/INSTALLATION.md`。
- 新增 Codex 本地安装脚本：`scripts/install_codex_skill.py`。
- 新增安装脚本测试：`tests/test_install_codex_skill.py`。

### Removed

- 删除 Cursor / Trae 适配入口，避免对外呈现不再优先维护的客户端支持范围。
- 删除重复的多 Agent 兼容说明文档：`docs/AGENT_COMPATIBILITY.md`。

### Verified

- `python scripts\validate_repo.py`
- `python -m unittest discover -s tests -v`
- `python skills\kaoyan-english\scripts\audit_corpus.py --skill skills\kaoyan-english`
- Codex skill quick validate
