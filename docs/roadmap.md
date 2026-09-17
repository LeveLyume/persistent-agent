# Persistent Agent Roadmap

> 更新：2026-09-17。本文区分已验证基线与候选开发方向；下一 Development Version 尚未由 Owner 定义。开发管理编号遵循 [AGENTS.md](../AGENTS.md)：Development Version 为 `v0.X`，Task Version 为 `v0.X.Y`。它们不自动等于 `pyproject.toml` 包版本、Git Tag 或正式发布。

## 1. 项目愿景

逐步形成可持续运行、可替换模型、有长期记忆、可调用工具并作用于受控环境的 Agent；Identity、Relationship、State 各有边界，未来可扩展到桌面角色、语音、视觉和具身交互。结构与边界见 [architecture.md](./architecture.md)。

## 2. 当前状态

**已完成的 v0.0 基线：** 仓库骨架与 Git 历史、Python 项目配置、CLI 入口、OpenAI 兼容模型适配器、基础 Runtime、Context Builder、进程内 Working Memory、连续对话、`/reset`、`/exit`。工作日志记录本地 Python 虚拟环境与真实 DeepSeek 回复的历史用户反馈；当前代码按配置调用该接口。

**待核验或证据有限：** 分支、最近提交和远端同步状态随每次提交变化，须以当次 Git 检查为准，不在 Roadmap 固定 HEAD。README 与工作日志已入库；远端状态需在推送后实时核验。具体已安装依赖版本只有工作日志中的历史本地快照，`pyproject.toml` 未锁定版本。工作日志记录离线模拟路径通过，但异常路径未专项覆盖；仓库当前没有自动化测试套件。真实 API 成功是历史反馈，本次文档编辑未重测。

**尚未实现：** 长期记忆、SQLite Memory Store、Embedding、自动提取、工具调用循环、Environment 路径约束、Identity / Relationship / State 的实际行为、Web / Desktop / Voice / Avatar。

## 3. 当前基线版本：v0.0 — Initial Working Baseline

**状态：** 已完成（历史回溯）；不是新开发版本的批准。项目包版本 `0.1.0` 与此编号无关。

```text
User Input → CLI → AgentRuntime → ContextBuilder
                        ↑            ↑
                 WorkingMemory ───────┘
                        ↓
                 ModelProvider → DeepSeek → Response
```

历史用户反馈覆盖 CLI 正常流程，离线模拟补验覆盖历史裁剪、失败不写入、reset 等；详见 [work-log.md](./work-log.md)。限制是只有同步文本 CLI、会话随进程消失、20 轮不是 Token 预算、无长期 Memory 或工具能力。

## 4. 下一候选方向：Persistent Memory Foundation

**状态：规划候选，未获 Owner 定义为 `v0.1`。** 长期 Memory 是近期优先方向，但正式目标、范围与 Task Plan 须由 Owner 批准。以下 `v0.1.Y` 仅作可独立验收的拆分草案；不表示已开始或已分配正式编号。Memory 子系统能力阶段另用 `M1` 等，见 [memory-system-design.md](./memory-system-design.md)。

**进入条件：** Owner 确定 Development Version 的目标与范围；Codex 提交含 Version Finalization 的 Task Plan 并获一次性批准。**不在此候选范围内：** 工具循环、Web、语音、角色形象及高级关系记忆。

| 候选编号 | 任务与依赖 | 验收条件 | 建议提交（批准后按规范补编号） |
| --- | --- | --- | --- |
| v0.1.1 | Memory 数据模型、`MemoryStore` 协议与 schema 设计；起点 | 可构造且校验参数；协议不依赖 SQLite；Runtime 无数据库细节 | `feat(memory): define memory model and store protocol [v0.1.1]` |
| v0.1.2 | SQLite Store；依赖 .1 | 插入、按 ID 取、列出、删除；重启保持；连接生命周期与路径明确，数据库被 Git 忽略 | `feat(memory): add SQLite memory store [v0.1.2]` |
| v0.1.3 | MemoryService；依赖 .2 | Store 可替换；服务错误明确；Runtime 无 SQL | `feat(memory): add persistent memory service [v0.1.3]` |
| v0.1.4 | 手动 CLI 命令；依赖 .3 | `/remember`、`/memories`、`/forget` 可保存、查看、删除；重启保持；`/reset` 不删除长期记忆 | `feat(cli): add persistent memory commands [v0.1.4]` |
| v0.1.5 | 基础检索与 Context 注入；依赖 .4 | 新会话可使用相关记录；限制注入数与预算；标来源；Context Builder 不直读数据库 | `feat(memory): inject recalled memories into context [v0.1.5]` |
| v0.1.6 | Embedding 与基础排序；依赖 .5，是否纳入首版待 Owner 决定 | 改写查询仍能找到相关记忆；Provider 可换；API 故障明确；不把聊天接口当 Embedding 接口 | `feat(memory): add semantic memory retrieval [v0.1.6]` |
| v0.1.7 | 自动提取与评估；依赖 .4，可在 .6 后推进；是否纳入首版待 Owner 决定 | 寒暄不大量写库；明确偏好有候选；去重、更正、来源与敏感策略可验证 | `feat(memory): add memory extraction and evaluation [v0.1.7]` |
| v0.1.8 | Version Finalization；依赖该版本获批的所有任务 | 完整目标验证通过；README、设计和日志准确；收尾提交获批准并 push 后才可宣告版本完成 | `docs(project): finalize persistent memory foundation [v0.1.8]` |

若 Owner 将首版限定为 M1，可把 Embedding 与自动提取移至后续 Development Version，并重新编号 Finalization；调整原因记录在工作日志。每任务只在测试、文档、原子 commit 和经批准的 push 完成后标记完成。

## 5. 后续候选版本

以下是**依赖顺序与完成定义**，不是已批准的版本编号、日期或同时开工的清单。

| 阶段 | 目标与依赖 | 完成定义 |
| --- | --- | --- |
| Tool and Environment | 在基础 Runtime 后加入 Tool 协议、Registry、安全内置工具、Workspace 路径约束、结构化结果 | Tool Call → 执行 → Result → Model 循环可测，越界路径被拒绝 |
| Identity、Relationship、State | 依赖明确的 Memory 边界与 Context 接口；加入稳定身份、关系和当前状态 | 服务职责分离，注入 Context 可测，不把事件记录混成当前状态 |
| Context Management | 依赖多来源上下文；Token 预算、裁剪、摘要与 Tool Result 管理 | 长对话在预算内稳定，来源与重要信息不丢失 |
| Interface Expansion | 依赖稳定 Runtime；Web、流式输出、会话管理、配置界面 | 新界面复用同一服务边界并通过端到端验证 |
| Persistent Character | 依赖成熟 Memory 与 Identity/Relationship/State；自传、关系、情感、整合、强化、关联与共同历史 | 有来源的跨重启、跨模型连续性可验证；用户可控制记忆 |
| Embodiment | 依赖受控 Environment 与扩展接口；Voice、Vision、2D Character、桌面交互 | Perception → Cognition → Action → Observation 循环受约束且可测试，保留 VLA 接口 |

## 6. 正式版本统一模板

仓库规则使用 `v0.X`，因此正式规划时采用下列格式；子任务使用 `v0.X.Y`。若以后改变编号体系，须由 Owner 决策并更新协作规范。

```markdown
## v0.X｜版本名称

**状态：** 规划中 / 进行中 / 已完成 / 受阻
**目标：**
**进入条件：**
**范围：**
**不在本版本范围内：**

| 编号 | 任务 | 状态 | 验收条件 | 提交 |
| --- | --- | --- | --- | --- |

**版本验收：**
**文档更新：**
**已知限制：**
```

正式 Task Plan 最后一项必须是 Version Finalization。每项执行代码检查、实现、匹配验证、自审、文档与工作日志、diff 检查、commit；每次 push 前汇报并取得 Owner 批准。

## 7. 状态定义

| 状态 | 含义 |
| --- | --- |
| 规划中 | 方向已提出，尚未开始；候选计划须另经 Owner 批准 |
| 进行中 | 已开始，尚未完成全部验收与提交推送 |
| 已完成 | 实现、验证、日志、commit 与批准后的 push 均完成 |
| 受阻 | 有明确阻碍需解决 |
| 待核验 | 有完成迹象，缺可重复证据 |
| 延后 | 已决定不进入当前版本 |

## 8. 优先级规则

当前基线已保存；下一候选优先级为长期 Memory 最小闭环，其后依次是 Tool 与 Environment、Identity / Relationship / State、Context Management、Web / Desktop、Voice / Vision / 2D Character、高级认知与具身扩展。Memory 优先是为了跨重启连续性，架构上仍由 Runtime 编排。优先级不构成开启新 Development Version 的授权。

## 9. 暂不实施

当前基线与近期最小 Memory 方向不提前实施 Multi-Agent、Planner、Reflection、Memory Graph、情绪模拟、Voice、Avatar、Computer Use、Docker/Remote Environment、VLA、自动部署或大规模分布式数据库。需要时保留接入位置，不预建空壳能力。

## 10. 版本结束规则

正式版本只有代码与验收命令通过、相关测试通过、敏感配置未入 Git、工作日志更新、README 反映用户可见变化、相关设计准确、commit 已创建、Owner 批准后的 push 已完成且限制已记录，才能标记已完成。仅有代码或本地 commit 时仍为进行中。Development Version 的 Finalization 还需覆盖整版目标并核对所有任务状态。
