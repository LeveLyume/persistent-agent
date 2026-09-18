# Persistent Agent 工作日志

> 更新日期：2026-09-18。按仓库实际代码、Git 历史和可重复验证结果记录；历史用户反馈单独标明。
> 开发协作规范见 [AGENTS.md](../AGENTS.md)，安装与使用见 [README.md](../README.md)。

## 当前进度

- **v0.0 — Initial Working Baseline：Completed / Retrospective（历史回溯完成）。**
- **v0.1 — 本地对话模型试运行：进行中。** Owner 已批准先部署本地对话模型，当前任务编号指定为 v0.1.1。
- **v0.1.1 — 本地 Qwen3 对话模型部署与接入：提交 `9a748b9` 已推送并核验，任务完成。**
- **v0.1.2 — 统一模型选择与本地服务生命周期：实施、验证和文档更新完成；任务完成仍以批准后的提交推送核验为准。**
- 已实现 CLI 连续对话、模型适配、Runtime、上下文构建、进程内 Working Memory、清空与退出、基础错误处理。
- 已新增便携 llama.cpp + Qwen3-0.6B Q8 本地模型，统一 CLI 可选择 DeepSeek 或本地 Qwen 并管理本地服务；GPU、CLI 与失败路径已实测，原 .env 未改动，测试服务已停止。
- 长期记忆、SQLite、记忆提取与检索、Embedding、工具调用、环境访问控制及 Identity / Relationship / State 尚未实现；对应源码为空白占位。
- **v0.0.4 — 基线文档整理与推送审批规范：已 commit 并 push，任务完成。**
- **v0.0.5 — 当前项目流程图与进度记录：已 commit 并 push。**
- **v0.0.6 — 协作规范维护：已 commit 并 push，任务完成。**
- v0.0.7、v0.0.8 的提交已在本轮开始时的本地 main 与本地 origin/main 引用历史中，分别为 `d87093d`、`38e975c`；本条不补造此前审批或实时远端查询记录。
- 原 Memory 的“v0.1.Y”属于未批准候选，现改用阶段编号并顺延；本轮采用 Owner 批准的本地模型目标。
- v0.0.4 历史整理开始时 HEAD 为 `6efb2db`；当时 Owner 的 AGENTS.md 修改经授权纳入该任务。本轮 v0.1.1 从 `main` 的 `38e975c` 开始，工作区干净。

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

**日期 / 文档状态：** 2026-09-17；文档更新完成。

**实际变更与决策：**

- 新增 `docs/diagrams/project-flow-v0.0.5.mmd`，按源码绘制 CLI 输入、配置、Runtime、会话历史、上下文、模型调用、成功保存及失败处理；单独标明未接入运行流程的占位模块。依 Owner 后续要求，将 Mermaid 文件归入独立的 `docs/diagrams/` 目录。
- README 增加流程图入口；工作日志将 v0.0.4 的旧待推送状态更正为已提交和推送，并记录证据边界。
- 保留 `pyproject.toml` 的包版本 `0.1.0`。它是安装包元数据，不等同于开发管理版本；本次没有修改运行代码、依赖或发布内容。
- Owner 补充要求工作日志直接写明文档更新完成，再申请 push；AGENTS.md 第 6 节已据此澄清文档更新与任务完成的区别，并规定工作日志最后编辑、之后只做必要的检查与提交推送流程。
- 因流程规范和图文件目录调整发生在本任务首次本地提交之后，分别追加提交记录调整；不改写已有提交。三项提交同属 v0.0.5，拟在同一次批准后推送。

**验证与限制：** 已核对 CLI、Runtime、Session、ContextBuilder、Model 及空白占位模块源码；流程图对应当前代码路径；README 链接指向现有 `.mmd` 文件；`git diff --check` 通过。Mermaid CLI 未安装，未做渲染检查；未运行真实模型 API，因本任务不修改运行代码。

**文档：** README 与工作日志已同步；空白的架构设计、记忆设计及 Roadmap 未受影响，无需更新。

**Commit messages：** `docs(project): record current flow and progress [v0.0.5]`；`docs(process): clarify work-log completion wording [v0.0.5]`；`docs(project): group Mermaid diagram in diagrams directory [v0.0.5]`。

**下一步：** 按规范汇报提交范围、SHA 和目标分支，申请推送批准；推送核验后再报告任务完成。随后等待 Owner 定义下一 Development Version。

## v0.0.6 — 协作规范维护

**授权与目标：** Owner 要求按已讨论的三个问题优化 `AGENTS.md`：限定文件范围、已完成版本的维护任务编号、diff 审阅与提交推送的边界。本任务是 v0.0 基线后的协作规范维护，不开启新的 Development Version。

**日期 / 文档状态：** 2026-09-17；规范与本条工作记录已更新，不以此表示 commit 或 push 已发生。

**实际变更与决策：** 已完成版本可在不改变产品目标时分配后续 `v0.X.Y` 维护任务；Owner 要求先看 diff 时允许停在“待审阅”，继续提交与 push 批准是两个独立节点；Owner 限定文件范围时遵守范围并报告未同步事项，工作日志未补齐前不宣称任务完成。等待审阅期间可处理 Owner 后续授权的独立任务，并隔离提交。

**验证与限制：** 对照原有版本规划、完成标准、Git 与工作日志条款检查一致性；`git diff --check -- AGENTS.md` 通过。本任务只修改协作规范和工作记录，无运行代码验证需求。先前由 Owner 要求仅编辑的三份设计文档仍有未提交工作区修改，本次提交不包含它们；其 README 占位说明尚待后续同步。

**文档：** `AGENTS.md` 与本日志更新；README 和三份设计文档在本任务中无需修改。

**Commit message：** `docs(process): clarify review and maintenance workflow [v0.0.6]`

**下一步：** 核对本任务的独立提交范围，推送前汇报并等待 Owner 明确批准；三份设计文档仍处待审阅状态。

**后续核验：** Owner 已批准推送 `d5ae5a009ae66d4f15df7c08f7f1f9bcdb0b1789`；`git push origin main` 成功，随后 `git ls-remote origin refs/heads/main` 与本地 HEAD 均指向该提交。此项记录在后续文档维护时补充，不改写原任务的提交。

## v0.0.7 — 设计文档与项目一致性规则

**授权与目标：** Owner 指出三份设计文档仍未提交，并要求修改 `AGENTS.md`，使每次开发形成完整 Git 循环、每次提交保持项目资料同步。本次将待审阅设计文档与其必要的 README、流程规范、工作日志同步纳入同一文档维护任务；不启动下一 Development Version。

**日期 / 文档状态：** 2026-09-17；文档更新与提交前核对完成。本段不表示 commit 或 push 已发生。

**实际变更与决策：** 完成 `architecture.md`、`memory-system-design.md` 和 `roadmap.md`，分别描述当前/目标架构、长期记忆设计与候选开发顺序；根据源码将占位模块标为未实现。README 不再称三份文件为空白。Roadmap 不固定易过时的 HEAD。`AGENTS.md` 增加提交前项目一致性检查、受影响文档同步、按路径暂存与完整暂存快照复查，以及推送后远端和工作区核验；限定文件范围与必要同步冲突时先解决，不提交已知不一致状态。

**验证与限制：** 对照 README、工作日志、`pyproject.toml`、相关源码、Git 历史与当前工作区核对已实现和规划状态；`git diff --check` 通过；五份变更文档的代码围栏配对、本地链接、敏感配置与旧占位描述已检查。Mermaid CLI 未安装，图未做渲染验证；未改运行代码，未重测真实模型 API。

**文档：** 三份设计文档、README、AGENTS.md 与本日志同步；既有流程图反映当前代码，无需更新。历史日志中“当时为空白”的表述保留为历史事实。

**Commit message：** `docs(project): synchronize design docs and commit workflow [v0.0.7]`

**下一步：** 检查最终暂存快照并提交；推送前向 Owner 报告提交 SHA、文件范围、验证限制与目标分支，等待批准。长期记忆等功能仍未实现，下一 Development Version 仍由 Owner 定义。

## v0.0.8 — 提交说明使用中文描述

**授权与目标：** Owner 要求提交说明的改动内容使用中文，保留 `type(scope)` 写法及版本号位置，并明确本次维护编号为 v0.0.8。

**实际变更与决策：** `AGENTS.md` 将提交格式中的描述占位符改为“中文描述”，要求用中文说明实际变化；提交类型、scope 和版本号位置不变。本任务只调整协作规范，不改变项目功能或开发阶段目标。

**验证与限制：** 核对 `AGENTS.md` 第 5 节的前后差异及 Git 工作区范围，`git diff --check` 通过。仅修改文档，无运行代码验证需求。

**文档：** `AGENTS.md` 与本工作日志已同步；README、架构设计、Memory 设计和 Roadmap 的事实内容不受影响，无需更新。

**Commit message：** `docs(process): 规定提交说明使用中文描述 [v0.0.8]`

## Development Version：v0.1 — 本地对话模型试运行

**目标 / 状态：** 在现有 CLI 中试用本机 Qwen3-0.6B 对话模型，验证实际运行与可恢复性；进行中。Owner 于 2026-09-18 批准执行，并指定当前任务为 v0.1.1，要求做好回退并更新工作日志。

### Task Plan

- [x] v0.1.1 — 便携模型部署、现有链路接入、实测与回退说明；提交推送及远端核验完成。
- [ ] v0.1.2 — 统一 CLI 选择 DeepSeek / 本地 Qwen，自动启停本地服务并整理文件；实施与验证通过，完成勾选以批准后的 push 核验为准。
- [ ] v0.1.3 — Version Finalization：覆盖整版验证，核对任务与资料，完成收尾提交及批准后的推送。

**计划调整：** 原 Roadmap 的长期记忆 v0.1.Y 只是候选，Owner 决定先做本地模型；Memory 改用候选阶段号，后续版本另行确定。实现检查确认兼容适配器和既有环境变量优先规则已够用，因此以独立脚本覆盖子进程配置，取消原草案中可能需要的核心配置/适配器修改。未引入新 Provider、Runtime 或 Python 依赖。

**后续计划调整：** v0.1.1 推送后 Owner 指出部署与统一使用入口应属同一版本目标，指定 v0.1.2 实现统一模型选择并整理文件。因此原 v0.1.2 Version Finalization 顺延为 v0.1.3；版本目标仍是本地对话模型可实际使用，本次补齐入口，不加入长期记忆。

### v0.1.1 — 本地 Qwen3 对话模型部署与接入

**日期 / 文档状态：** 2026-09-18；实施、验证和文档更新完成。本记录不表示本任务的 commit 或 push 已发生。

**实际变更：**

- 新增 `scripts/local_model.py`，提供 `setup`、`serve`、`chat`：固定版本下载、SHA256 校验、解压路径检查、便携服务启动、既有 CLI 本地配置注入。
- 本机部署官方 Qwen3-0.6B Q8（639446688 字节，修订 `23749fefcc72300e3a2ad315e1317431b06b590a`），llama.cpp b10964（程序报告 0.4.1-dev / b29c606e2）与 CUDA 13.3 便携 DLL。全部放入已忽略的 `data/local-model/`，含下载包约占 1.76 GiB；来源、校验值见 `docs/local-model.md` 和本机 manifest。
- `serve` 只监听 127.0.0.1:18080，随机本地密钥认证、限定 CORS、关闭 Web UI、使用离线模式；上下文 4096、单会话、输出最多 512 Token、关闭思考、8 线程、batch 256 / ubatch 128、额外主机提示缓存禁用。
- `chat` 复用原 `interfaces.cli`，仅给子进程设置三项模型配置；原 `.env`、父进程环境、核心对话代码和项目依赖保持原样。服务与 CLI 分开启动，退出 CLI 后仍需停止服务。
- 新增 5 项自动化测试，覆盖回退相关的配置隔离、无效下载保留、解压越界拒绝、绑定与资源限制、HTTP 错误及截断不污染会话。测试使用标准库 HTTP 服务，不额外安装测试依赖。

**回退与工程决策：** 采用项目内便携目录，不安装系统服务、驱动或全局包，不修改 PATH、注册表、防火墙或自启动。下载包先校验再启用，记录 manifest；本地访问密钥和模型不提交 Git。恢复远端只需停止本地服务并使用原 CLI 命令；卸载限定为 `data/local-model/`，仓库变更可通过本任务提交的 revert 撤销。没有执行破坏性清理。测试进程均已停止，原 .env 前后 SHA256 相同。

**验证结果：**

| 检查 | 结果与边界 |
| --- | --- |
| 离线自动化测试 | `.venv/Scripts/python.exe -m unittest discover -s tests -v`，5 项通过；含两个失败响应子案例 |
| GPU 加载 | RTX 5070 Laptop GPU 8151 MiB，驱动 610.47；日志确认 CUDA0、29/29 层上 GPU |
| 本地真实 API / CLI | 健康检查、模型列表、三轮回复、姓名追问、reset、exit 通过；无密钥访问返回 401 |
| 超长输入 / 停服 | 12063 Token 请求被 4096 限制返回 HTTP 400，CLI 可继续退出；停服后显示连接失败 |
| 最终实测 | 服务就绪 1.110 秒；三轮 CLI 总耗时 1.799 秒（含启动）；非通用性能基准 |
| 显存与停止回退 | 整卡启动前 1914 MiB、约 0.2 秒采样峰值 3107 MiB、停止后 1909 MiB；包含桌面和其他进程，不是进程精确峰值 |
| 运行库内存日志 | CUDA 模型缓冲区 604.15 MiB、KV 448.00 MiB、计算缓冲区 7.50 MiB |
| 配置与文件隔离 | .env 校验值未变；模型、密钥、日志和部署目录被 Git 忽略；核心源码与依赖声明无 diff |
| 资料自审 | Markdown 围栏、UTF-8、本地链接、敏感值检查通过；工作日志编辑前的 diff 检查通过，最后执行暂存快照检查 |

**问题与限制：** 首轮测试曾出现“1加1”回答为“1”，后续最终配置测试回答正确；0.6B 回复质量不可靠，接口通过不代表能力验收。未测长时间运行、并发或 Embedding 共存；原 DeepSeek 真实 API 未调用。20 轮历史没有 Token 预算，长输入需缩短或 reset，输出截断沿用现有不保存策略。初始化测试曾依赖当前环境不存在的 `httpx` 名称（已有 SDK 使用 httpx2），已改为标准库本地 HTTP 测试并通过，未修改环境依赖。初次 PowerShell HTTPS 读取受限、GitHub API 限流，后改用 Python 标准库读取官方发布页和下载，SHA256 均核对通过。

**文档同步：** README 增加本地入口、条件和测试；`docs/local-model.md` 包含安装、停止、回退、固定来源及实测；架构说明增加本地同协议服务；Roadmap 换成本轮计划并保留 Memory 候选；Memory 设计仅同步阶段状态。原 v0.0.5 流程图使用通用“配置的模型 API”，核心流程未变，无需修改。AGENTS.md、`.env.example`、`pyproject.toml` 无需更新，无包版本、Tag 或 Release 操作。

**Commit message：** `feat(model): 接入可回退的本地Qwen3对话模型 [v0.1.1]`

**下一步：** 按规范核对提交快照并汇报推送范围；经 Owner 单独批准 push 并核验后，才推进 v0.1.2 Version Finalization。

**后续推送核验：** Owner 已批准推送 `9a748b9f9e297534ff5341bcd4fdfa4663d9dc80`；`git push origin` 成功，随后 `git ls-remote origin refs/heads/main` 与本地 HEAD 均指向该提交，工作区干净。本条在 v0.1.2 文档维护中补充，不改写 v0.1.1 提交。

### v0.1.2 — 统一模型选择与本地服务生命周期

**授权与目标：** Owner 要求将本地模型接入的使用入口统一，整理相关文件，并指定任务编号 v0.1.2。用户从一个 CLI 选择 DeepSeek 或本地 Qwen；选择本地时同一进程启动与关闭便携服务，省去双窗口操作。

**日期 / 文档状态：** 2026-09-18；实施、验证及文档更新完成。本记录不表示本任务的 commit 或 push 已发生。

**实际变更与决策：**

- `interfaces/cli.py` 成为统一入口：启动菜单选择模型，`--model deepseek|local` 支持直接指定，`--setup-local` 执行首次部署或校验。DeepSeek 仅在被选中时读取原 `.env`，本地模式读取独立密钥文件。
- 将原 `scripts/local_model.py` 移入 `model/local_model.py`，保留固定版本下载、SHA256 校验与受限服务参数，新增 `LocalModelServer` 管理本次 CLI 启动的子进程及健康等待；退出、输入中断或启动失败时清理该进程，不按名称结束其他程序。
- 保留现有 Runtime、Context Builder、Working Memory 与 OpenAI 兼容适配器；没有新增模型协议、核心依赖、包版本或系统级安装。原数据目录与模型文件保持原位，无迁移或重下载。
- 原五项测试改为从包内导入本地部署模块；新增三项模型选择测试，覆盖本地模式跳过远端配置且关闭服务、DeepSeek 模式不启动本地服务、启动失败不创建模型客户端。

**验证结果与限制：** `python -m unittest discover -s tests -v` 共 8 项通过。统一 CLI 菜单选择本地模式后，真实 Qwen 模型完成姓名追问、`/reset`、`/exit`；退出后本地端口关闭，整卡显存由试跑前 2186 MiB 回到 2166 MiB。菜单选 DeepSeek 可进入并退出，但本次未调用真实远端 API；错误选择会提示重选。模拟 Ctrl+C 退出亦确认子进程停止、端口释放。`--setup-local` 重验三个已下载文件的 SHA256 成功，未替换本地密钥。原 `.env` 前后 SHA256 相同。回复质量与 4096 Token 上下文限制沿用 v0.1.1 的实测边界；未做长时或并发评估。

**文档同步：** README 改为单入口步骤与模型菜单；`docs/local-model.md` 更新自动启停、回退与新增验证；架构文档同步 CLI 选择与本地模型模块边界；Roadmap 记录新增 v0.1.2 和顺延的 v0.1.3。长期记忆设计及 v0.0.5 历史流程图未改变，无需更新。AGENTS.md、`.env.example`、`pyproject.toml` 无需修改。

**Commit message：** `feat(cli): 统一选择模型并自动管理本地服务 [v0.1.2]`

**下一步：** 完成最终暂存快照核对并提交；推送前汇报本任务范围、验证、目标提交与远端，等待 Owner 单独批准。随后执行 v0.1.3 Version Finalization。

## 历史候选方向（未批准为当前版本）

原 V0.1 设想包含 CLI、模型接入、工具循环、长期记忆保存与检索、上下文注入和本地持久化；其中 CLI 和模型接入已落实，其余仍为规划。

此前讨论的记忆推进顺序是：数据结构 → SQLite → MemoryService → 手动保存/读取/删除及重启验证 → 检索与上下文注入 → Embedding。`/remember`、`/memories`、`/forget` 是候选命令，当前不支持；Embedding Provider 尚未确定。未来 /reset 只清空会话、不删除长期记忆，是历史设计意图，尚无长期记忆实现可验收。

后续架构继续复用既有 Runtime、Session、Context Builder 和 Model Adapter。长期角色连续性由 Identity、Memory、Relationship、State 共同支撑，不能等同于某个 LLM。`workspace/` 仅是目录约定，访问控制仍需实现；本地数据被 Git 忽略，未来涉及数据迁移时需单独考虑备份。
