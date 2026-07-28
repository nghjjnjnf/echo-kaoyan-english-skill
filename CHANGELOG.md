# 修改记录

本项目从 2026-07-28 起使用此文件记录每次对外可见的修改。后续提交应在提交前补充对应条目，说明做了什么、影响哪些客户端或功能、验证了什么。

## 2026-07-28

### Changed

- 启动提示和跨客户端入口加入“旧版回答过于简略”的已知失败模式提醒，要求首次使用时也必须先加载对应题型模板并完整作答。
- 宽泛真题请求不再允许走普通简答路径：当用户只说“解析某年阅读理解/完形”等宽泛问法时，规则会先解析英一/英二、年份和题型，再按答案表加首批详细解析执行。
- Codex、Claude Code 和通用 Agent 入口同步加入宽泛请求处理策略，要求阅读按 Text/题号分批精讲，完形按 1-5 空起步精讲，只有用户明确要求简答时才输出概览或答案-only。
- 阅读和完形选项讲解改为排除法优先：错误选项必须详细说明迷惑点、失配位置、排除依据和陷阱类型，不能一句话带过。
- 阅读和完形的原文截取规则升级：定位句或空格句不能孤立展示，默认引入同段前三句和后三句；不足或越界时展示整段。
- 新增 `references/index.json` 快速检索索引，可按英一/英二、年份、题型和题号直接定位真题文件与答案；检索流程优先使用该索引。
- 增加模板合规门槛：所有 rubric 输出前必须按固定标题自检，阅读和完形禁止省略、改名或合并必需模块。
- 完形解析 rubric 新增专业风格参考模板，要求围绕空格线索、趋势链、搭配语法和选项陷阱展开教师式讲解。
- 阅读解析 rubric 新增专业风格参考模板，要求阅读回答参考教师式证据链讲解、同义替换映射和完整陷阱分析。
- 阅读题意图识别加强：将“选什么/为什么这么选/第几个为什么选”等真实学生问法默认路由到完整阅读解析格式，只有明确要求“只告诉答案”时才简答。
- README 首页图改用新的 `hero-kaoyaner.svg` 路径，避免 GitHub 对旧 SVG 路径的缓存继续显示旧文案。
- README 将“核心亮点”改为“核心能力”，并重写为更面向学习者收益的项目介绍。
- README 首页主视觉图文案调整为 `SKILL · for 考研er`，让定位更贴近备考用户。
- README 典型用法改为更贴近真实用户提问的自然表达，避免把内部输出格式规则写进示例 prompt。
- README 快速开始补充最简单使用方式：把 GitHub 仓库地址直接交给 Codex 或 Claude Code。
- README 导航栏和主要模块标题加入小图标，提升 GitHub 项目主页的可读性和视觉层次。
- 清理项目级内容边界旧说明，统一改为仓库数据边界、隐私数据和临时源文件边界说明。
- `.codex-plugin/plugin.json` 移除旧字段，`corpus-index.json` 移除 `content_scope` 字段，保持项目元数据更简洁。
- `skills/kaoyan-english/references/strategies/simulation-generation.md` 和 `fetch_source_article.py` 调整外刊来源说明，改为强调主题启发、事实核查和原创改编流程。
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

- 删除仓库根目录和 skill 内部的旧说明文件。
- 删除 Cursor / Trae 适配入口，避免对外呈现不再优先维护的客户端支持范围。
- 删除重复的多 Agent 兼容说明文档：`docs/AGENT_COMPATIBILITY.md`。

### Verified

- `python scripts\validate_repo.py`
- `python -m unittest discover -s tests -v`
- `python skills\kaoyan-english\scripts\audit_corpus.py --skill skills\kaoyan-english`
- Codex skill quick validate
