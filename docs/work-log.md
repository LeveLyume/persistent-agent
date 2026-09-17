# Persistent Agent 工作日志

> 更新日期：2026-09-17。按仓库实际代码、Git 历史和可重复验证结果记录；历史用户反馈单独标明。
> 开发协作规范见 [AGENTS.md](../AGENTS.md)，安装与使用见 [README.md](../README.md)。

## 当前进度

- **v0.0 — Initial Working Baseline：Completed / Retrospective（历史回溯完成）。**
- 已实现 CLI 连续对话、模型适配、Runtime、上下文构建、进程内 Working Memory、清空与退出、基础错误处理。
- 长期记忆、SQLite、记忆提取与检索、Embedding、工具调用、环境访问控制及 Identity / Relationship / State 尚未实现；对应源码为空白占位。
- **v0.0.4 — 基线文档整理与推送审批规范：已 commit 并 push，任务完成。**
- **v0.0.5 — 当前项目流程图与进度记录：文档已更新并核对，待本任务 commit / push，尚未完成。**
- 下一 Development Version 尚未由 Owner 定义。旧文档的“V0.1”属于历史路线，不作为当前授权计划。
- 本次整理开始时，分支为 `main`，HEAD 为 `6efb2db`；工作区已有 Owner 对 `AGENTS.md` 的未提交修改，随后 Owner 授权调整推送审批规则，本次将规范与两份文档共同纳入 v0.0.4。

## 记录与版本说明

旧开发发生在版本化协作规范建立之前。以下 `v0.0.1～v0.0.3` 是按真实提交做的回溯映射，不表示当时执行过 Task Plan 审批、逐任务验收或 Version Finalization。没有补建 Tag、重写提交或调整包版本。

`pyproject.toml` 的 `0.1.0` 是第二次提交写入的包元数据，与开发管理版本分开。历史提交保留原始 message；新 Development Version 按 AGENTS.md 执行，由 Owner 定义、Codex 拆解，最后包含 Version Finalization。

本日志重构合并了旧记录中的重复说明和操作模板，保留实际事件、工程决策、问题、验证限制和历史规划。原始日志完整版本可通过 `git show 4c38584:docs/work-log.md` 查看；下述更正不代表历史当时已有相应核验。

## Development Version：v0.0 — Initial Working Baseline

**目标：** 从项目骨架建立可运行的最小交互 Agent，并同步公开使用说明。

**状态：** 历史回溯完成；不等于长期持久化 Agent 已完成，也不等于所有异常路径通过测试。

### Task Plan（回溯映射）

- [x] v0.0.1 — Project Bootstrap：创建项目骨架。
- [x] v0.0.2 — Minimal Interactive Agent：实现最小连续对话链路。
- [x] v0.0.3 — README Synchronization：同步使用说明与能力边界。

**计划说明：** 以上由三次历史提交归纳，不是当年的预先批准计划；没有独立的历史 Version Finalization 提交，不补造该记录。

### v0.0.1 — Project Bootstrap

**日期 / 状态：** 2026-09-16（提交日期，UTC+8）；历史任务完成。旧日志将筹备阶段记为 2026-09-15～09-16。

**目标：** 建立仓库、Python 包目录及后续模块边界。

**实际变更：** 根提交新增 54 个文件、63 行内容：

- 建立 `src/persistent_agent/` 包及各模块的空白 Python 文件。
- 新增 `.gitignore`，排除虚拟环境、缓存、真实 `.env`、本地数据、工作区及日志。
- 新增三项配置键的 `.env.example`，当时值均为空。
- 新增初始 README，明确仅有骨架、无可运行功能。
- `pyproject.toml`、`AGENTS.md` 和三份设计文档当时均为空。

**工程决策：** 提前划分 Runtime、Model、Session、Memory、Tools、Environment 等模块，但占位不作为实现；此时还没有有效的打包配置或依赖声明。

**验证与限制：** 2026-09-17 通过根提交 diff 核实文件内容和范围。创建仓库、首次 push 成功来自旧日志中的用户反馈；Git 不保存虚拟环境，也不跟踪空目录，不能由该提交推断环境或程序已可运行。

**文档：** 初始 README 写入项目目标和旧 V0.1 设想；当时尚无工作日志。

**Git：** `6b78874` — `chore: initialize project structure`。已包含在 2026-09-17 核验的远端 main 历史中。

**后续：** 当时需建立真实模型调用和正式交互链路，见 v0.0.2。

### v0.0.2 — Minimal Interactive Agent

**日期 / 状态：** 2026-09-16；历史任务完成，正常交互路径有用户验收反馈。

**目标：** 将临时 API 连通性验证整理为模块化的 CLI 连续对话程序。

**实际变更：** `git diff 6b78874 4c38584` 共 11 个文件，新增 625 行、删除 2 行。下面的 Python 路径相对于 `src/persistent_agent/`。

| 文件 | 实际变更 |
| --- | --- |
| `pyproject.toml` | 从空文件建立 setuptools 配置，包版本 0.1.0，Python >=3.11，依赖 openai / python-dotenv，从 src 发现包 |
| `.env.example` | 保留空密钥，补入 DeepSeek 地址和历史聊天模型示例 |
| `core/types.py` | 不可变 Message，支持 system / user / assistant 文本消息 |
| `config/settings.py` | 加载指定 .env，检查三项必填值；已有环境变量优先；密钥不进入 repr |
| `model/base.py` | ModelProvider.generate 协议及统一 ModelError |
| `model/openai_compatible.py` | 兼容 API 调用；60 秒超时、无自动重试；基础服务异常转换、空回复和长度截断检查、客户端关闭 |
| `session/working_memory.py` | 默认保留最近 20 个完整问答轮次，历史副本、清空、轮数合法性检查 |
| `cognition/context_builder.py` | 组装系统提示、会话历史和本轮输入 |
| `runtime/agent_runtime.py` | 调用上下文构建与模型，仅成功后保存问答；支持 reset_session |
| `interfaces/cli.py` | 配置和组件组装、连续输入、空输入跳过、错误展示、/reset、/exit、中断及 EOF 退出和客户端关闭 |
| `docs/work-log.md` | 首次加入工作日志，记录筹备、环境、连通性、配置故障及正常路径验收反馈 |

**重要工程决策：**

- Runtime 依赖 ModelProvider 接口，模型供应商适配独立；未另建平行运行链路。
- 会话仅保存在进程内存；失败、空回复或长度截断的请求不保存为正常轮次。
- 使用同步文本调用；没有流式输出、异步任务或专门的请求取消机制。
- 20 轮是轮数裁剪，不是 Token 预算，单条消息仍可能过长。
- CLI 使用 `Path.cwd() / ".env"`，启动约定为项目根目录；系统提示暂在 CLI 中定义，明确没有长期记忆和工具。
- ModelProvider 目前为文本输入输出协议，未来工具调用需另行设计协议扩展。

**历史环境与验证：**

- 用户创建 `.venv` 并反馈 Python 3.13.7，随后反馈收到真实 DeepSeek 回复。临时 API 检查没有独立源码存档，不推断已提交临时脚本。
- 安装和正式 CLI 正常流程收到“全部流程跑通”的整体反馈，覆盖启动、至少两轮对话、姓名回忆、/reset 和 /exit；没有逐项终端输出存档。
- 当时未专项验证配置缺失、认证/限流/超时/连接/HTTP 错误、空回复、长度截断、轮数边界和 Ctrl+C / EOF。2026-09-17 的离线补验单列在后文，不回写成当时已通过。

**问题 BUG-001：** 临时配置检查曾出现 `KeyError: 'LLM_API_KEY'`。当时建议检查工作目录、.env 文件名和内容；之后用户反馈请求成功。现象已解决，具体根因及实际修复未记录，不能认定为某一种原因。正式 Settings 已加入必填项检查。

**文档：** 新增工作日志；README 在本次提交未修改，仍描述骨架状态，由下一提交同步。三份设计文档仍为空。

**Git：** `4c38584` — `短连续对话和会话清空；长期记忆、工具调用还没有实现`。已包含在核验的远端 main 历史中。旧日志建议的 `feat: implement CLI chat with session memory` 不是实际提交说明。

### v0.0.3 — README Synchronization

**日期 / 状态：** 2026-09-16；历史任务完成。

**目标：** 让公开说明与已实现的最小交互链路一致。

**实际变更：** `git diff 4c38584 6efb2db` 仅修改 README，新增 207 行、删除 16 行；补充能力和未实现项、配置安装启动、CLI 命令、架构及目录、旧路线和开发原则。没有修改运行代码。

**工程决策：** 区分会话记忆与长期记忆，明确目录占位不代表功能完成。

**验证与限制：** 本次通过提交 diff 确认仅有 README 变化；该提交没有增加测试或新的运行验收证据。

**文档：** README 已同步；工作日志保留第二次提交时的旧内容，因此其中“源码、Git 和 push 待核验”等表述在后续已过时，见下方更正。

**Git：** `6efb2db` — `更新了README，未修改其他代码`。2026-09-17 远端 main 核验结果为该提交。

## v0.0.4 — 基线文档整理与推送审批规范

**授权与目标：** Owner 要求接续进度，并按实际 commit diff 重构 README 与工作日志。随后 Owner 明确要求所有文件修改以 commit + push 闭环，并在每次 push 前汇报等待批准。据此分配 v0.0.4，作为 v0.0 基线的文档维护任务；不属于前三项历史回溯，也不启动 v0.1。

**日期 / 状态：** 2026-09-17；文档修改及验证完成，已提交并推送，小版本完成。

**开始状态：** 交接核验时本地工作区干净，本地和远端 main 均为 `6efb2db`。开始本次文档编辑时，Owner 已修改 `AGENTS.md`；最初保留该修改；本次依 Owner 最新指令，在既有规范上调整审批和完成规则并共同提交。

**实际变更与决策：**

- README 保留安装和使用入口，更新版本含义、真实运行流程、能力边界、配置说明和设计文档占位状态；旧 V0.1 清单改为未批准的后续方向。
- 工作日志按 Development Version → Task Version → 目标 / 变更 / 决策 / 验证 / 文档 / Git 重构，保留历史事件和不确定性。
- 更正初始提交的含义：它建立的是包骨架，打包配置和可运行功能均在第二次提交加入。
- 更正旧“尚未检查源码、提交及推送”的当前状态：现已检查源码和三次 diff，远端 main 包含全部历史提交；不推断各次 push 的具体发生时间。
- 保留旧长期规划及 BUG-001，删除重复操作模板和已失效的“下一步先保存已提交代码”指引。
- AGENTS.md 明确所有文件修改必须 commit + push；小版本以二者成功为完成标记；每次 push 前汇报并等待 Owner 批准，替换原先“计划批准后自动推送”的约定。
- 本次没有功能、依赖或架构变更；三份设计文档无需更新。

**核验记录：**

| 检查 | 结果与证据边界 |
| --- | --- |
| Git 状态、历史及远端 main | 本地 HEAD 与 `git ls-remote origin refs/heads/main` 均为 `6efb2db04e1f357a3e902c3796fd6316656a7aed`；首次沙箱内查询失败，随后沙箱外只读查询成功 |
| 核心源码、占位文件及 tests | 核心八个 Python 模块有实现；长期系统仍为空白占位；tests 中无测试文件 |
| 本地解释器与依赖 | Python 3.13.7；openai 3.14.1；python-dotenv 1.2.3。仅为本地安装快照，不是锁定依赖版本 |
| 密钥文件 Git 状态 | `.env` 被忽略且未被跟踪；未输出密钥内容 |
| 离线模拟模型检查 | 模块导入、多轮上下文、失败不写入历史、reset、20 轮裁剪及 snapshot 副本隔离均通过 |
| 文档自审 | 三次提交的变更范围已核对；README 和工作日志的 UTF-8、代码围栏配对、本地链接及 `git diff --check` 检查通过 |
| 真实 API 和 CLI 端到端 | 本次未重测，沿用 2026-09-16 的用户反馈，不扩大为全部异常路径通过 |

离线检查使用终端临时脚本及模拟 ModelProvider，没有新增持久化测试套件。尚未覆盖供应商异常转换、缺失配置、空回复、长度截断及 CLI 中断等专项路径。

**Commit message：** `docs(project): align baseline records and require push approval [v0.0.4]`

**Git 与审批状态：** 提交 `a883b8e333bb59c028589f9ca944ee2f4de1af14` 包含 AGENTS.md、README.md、docs/work-log.md。本地 `refs/remotes/origin/main` 的 reflog 记录于 2026-09-17 13:18:47 +0800 由 push 更新至该提交；本次核对时本地 HEAD 与 origin/main 均为该 SHA，工作区干净。2026-09-17 再次实时查询 GitHub 远端时遇到系统凭据错误，因此没有把该查询记作成功核验。

**下一步：** Owner 随后要求补齐当前进度记录与带版本号的 Mermaid 流程图，作为 v0.0 的文档维护任务 v0.0.5；仍未开启长期记忆功能开发。

## v0.0.5 — 当前项目流程图与进度记录

**授权与目标：** Owner 要求更新工作日志进度、更新版本号，并生成文件名带版本号的 Mermaid 图。本任务沿用已完成的 v0.0 基线，分配文档维护小版本 v0.0.5；不改变功能范围或开启下一 Development Version。

**日期 / 状态：** 2026-09-17；文档修改及核对完成，待 commit、推送审批和 push，任务尚未完成。

**实际变更与决策：**

- 新增 `docs/project-flow-v0.0.5.mmd`，按源码绘制 CLI 输入、配置、Runtime、会话历史、上下文、模型调用、成功保存及失败处理；单独标明未接入运行流程的占位模块。
- README 增加流程图入口；工作日志将 v0.0.4 的旧待推送状态更正为已提交和推送，并记录证据边界。
- 保留 `pyproject.toml` 的包版本 `0.1.0`。它是安装包元数据，不等同于开发管理版本；本次没有修改运行代码、依赖或发布内容。
- 按 Owner 的编辑顺序偏好，在流程图和 README 核对后最后编辑工作日志。尚未发生的本次 commit / push 不提前记为完成；按 AGENTS.md 第 6 节在提交中记录当时真实状态，推送结果在后续任务的日志更新时同步。

**验证与限制：** 已核对 CLI、Runtime、Session、ContextBuilder、Model 及空白占位模块源码；流程图对应当前代码路径；README 链接指向现有 `.mmd` 文件；`git diff --check` 通过。Mermaid CLI 未安装，未做渲染检查；未运行真实模型 API，因本任务不修改运行代码。

**文档：** README 与工作日志已同步；空白的架构设计、记忆设计及 Roadmap 未受影响，无需更新。

**Commit message：** `docs(project): record current flow and progress [v0.0.5]`。

**下一步：** 完成本地提交，按规范汇报提交 SHA、文件范围和目标分支，等待 Owner 明确批准后推送并核验。随后等待 Owner 定义下一 Development Version。

## 历史候选方向（未批准为当前版本）

原 V0.1 设想包含 CLI、模型接入、工具循环、长期记忆保存与检索、上下文注入和本地持久化；其中 CLI 和模型接入已落实，其余仍为规划。

此前讨论的记忆推进顺序是：数据结构 → SQLite → MemoryService → 手动保存/读取/删除及重启验证 → 检索与上下文注入 → Embedding。`/remember`、`/memories`、`/forget` 是候选命令，当前不支持；Embedding Provider 尚未确定。未来 /reset 只清空会话、不删除长期记忆，是历史设计意图，尚无长期记忆实现可验收。

后续架构继续复用既有 Runtime、Session、Context Builder 和 Model Adapter。长期角色连续性由 Identity、Memory、Relationship、State 共同支撑，不能等同于某个 LLM。`workspace/` 仅是目录约定，访问控制仍需实现；本地数据被 Git 忽略，未来涉及数据迁移时需单独考虑备份。
