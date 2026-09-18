# Persistent Agent

一个面向长期运行和持续扩展的 Agent 项目。

项目将 Runtime、模型、会话、长期记忆、工具和执行环境划分为独立模块，并为 Identity、Relationship、State 等角色连续性能力保留扩展空间。

## 当前状态

**当前开发：v0.1 — 本地对话模型试运行（进行中）。** v0.1.1 已完成便携部署并推送；v0.1.2 正在统一模型选择与启动入口；v0.1.3 为 Version Finalization。v0.0 CLI 基线已完成（历史回溯）。`pyproject.toml` 中的包版本 `0.1.0` 不等同于开发版本。

已经实现：

- 基于 CLI（命令行界面）的连续对话
- 通过 OpenAI 兼容接口调用 DeepSeek
- 使用便携 llama.cpp 服务调用本地 Qwen3-0.6B Q8 对话模型（Windows NVIDIA GPU 已实测）
- 统一 CLI 启动时选择 DeepSeek 或本地 Qwen3；选择本地时自动启动并停止模型服务
- 当前会话历史记录（默认最多保留最近 20 个完整问答轮次）
- 上下文构建
- `/reset` 清空当前会话
- `/exit` 正常退出
- 基础配置检查与模型调用错误处理

目前尚未实现：

- 跨程序重启的长期记忆
- SQLite 记忆存储
- 记忆检索与上下文注入
- 自动记忆提取
- 工具调用循环
- 本地工作区访问控制
- Identity、Relationship、State 系统
- Web 或桌面界面

> 当前的 Working Memory 只存在于程序内存中。关闭程序或执行 `/reset` 后，会话历史会丢失。

## 架构概览

当前运行流程：

```text
CLI → AgentRuntime
        ├─ 读取 WorkingMemory 的历史副本
        ├─ ContextBuilder：系统提示 + 历史 + 当前输入
        ├─ ModelProvider → OpenAICompatibleModel → DeepSeek 或本地 llama.cpp API
        └─ 成功后保存本轮问答到 WorkingMemory → 返回回复
```

项目长期规划中的核心组成包括：

| 模块         | 职责                          |
| ------------ | ----------------------------- |
| Runtime      | 编排一次完整的 Agent 交互流程 |
| Model        | 对接可替换的大语言模型服务    |
| Session      | 保存当前会话和 Working Memory |
| Cognition    | 构建模型本轮需要的上下文      |
| Memory       | 保存和检索跨会话长期记忆      |
| Capabilities | 管理工具及其他能力            |
| Environment  | 管理工具作用的执行环境        |
| Identity     | 管理 Agent 的稳定身份         |
| Relationship | 管理 Agent 与用户的关系状态   |
| State        | 管理 Agent 当前的内部状态     |

## 环境要求

- Python 3.11 或更高版本
- Git
- 远端模式需要 DeepSeek API Key；本地模式需要已部署的模型服务
- Windows PowerShell（以下命令以 Windows 为例）

已核验的开发环境为 Windows / PowerShell / Python 3.13.7；其他平台尚未验证。运行依赖由 `pyproject.toml` 声明：`openai`、`python-dotenv`，目前未锁定版本。

## 安装

克隆仓库并进入项目目录：

```powershell
git clone https://github.com/LeveLyume/persistent-agent.git
cd persistent-agent
```

创建虚拟环境：

```powershell
py -m venv .venv
```

以可编辑模式安装项目及依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

`-e` 表示可编辑安装。修改普通 Python 源码后，只需重新启动程序，不必再次安装。

## DeepSeek 配置

首次配置时复制模板；已有 `.env` 时直接编辑原文件：

```powershell
Copy-Item .env.example .env
```

打开项目根目录中的 `.env`，填写：

```dotenv
LLM_API_KEY=你的DeepSeek_API_Key
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=填写账户可用的聊天模型名称
```

模板当前包含历史模型示例；请填写实际可用的模型名称，不将模板视为服务商当前模型目录。程序从当前工作目录读取 `.env`，已有进程环境变量优先，三个配置项均不能为空。

真实 API Key 可通过本地 `.env` 或进程环境变量提供。

不要将 API Key 写进：

- `README.md`
- `.env.example`
- 源代码
- Git 提交记录

`.env` 已通过 `.gitignore` 排除，不应上传到 GitHub。

## 运行与模型选择

确保 PowerShell 当前位于项目根目录，然后执行同一入口：

```powershell
.\.venv\Scripts\python.exe -m persistent_agent.interfaces.cli
```

启动后输入 `1` 使用 DeepSeek，输入 `2` 使用本地 Qwen3-0.6B。选择本地时程序会启动本地服务；退出对话时会关闭由本次 CLI 启动的服务。首次在新电脑使用本地模型，先运行一次：

```powershell
.\.venv\Scripts\python.exe -m persistent_agent.interfaces.cli --setup-local
```

也可用 `--model deepseek` 或 `--model local` 跳过选择菜单。DeepSeek 使用 `.env`；本地模型使用 `data/local-model/` 中的密钥和模型文件，不读取 `.env` 中的 DeepSeek 密钥。

选择模型并启动后可以输入消息：

```text
你：我叫 LeveLyume，正在学习计算机。
Agent：……
```

继续询问时，程序会把当前会话历史一起发送给模型：

```text
你：我叫什么？正在学什么？
Agent：……
```

## 本地模型模式

本机已部署 Qwen3-0.6B Q8。统一入口选 `2` 即可使用。固定的便携构建适用于 Windows x64、兼容 CUDA 13.3 的 NVIDIA 驱动；详细安装条件、校验值、实测结果及回退步骤见[本地模型说明](docs/local-model.md)。

服务监听 `127.0.0.1:18080`，使用独立随机访问密钥；单会话、4096 Token 上下文、最多生成 512 Token、关闭思考模式。超长输入会报错，仍可用 `/reset` 清空历史。0.6B 的回复质量有限，已观察到简单算术误答。

## CLI 命令

| 命令     | 作用             |
| -------- | ---------------- |
| `/reset` | 清空当前会话历史 |
| `/exit`  | 退出程序         |

`/reset` 清空当前内存会话；目前没有长期记忆可供保留或删除。

当前采用同步文本回复，没有流式输出。请求失败的轮次不会写入历史；模型客户端配置 60 秒超时并关闭自动重试。20 轮限制不是 Token 预算，过长输入仍可能超过模型上下文限制。

## 项目结构

```text
persistent-agent/
├── docs/                       # 架构、路线和开发日志
├── src/
│   └── persistent_agent/
│       ├── core/               # 公共数据结构和协议
│       ├── config/             # 配置读取与检查
│       ├── runtime/            # Agent 主运行流程
│       ├── session/            # 当前会话与 Working Memory
│       ├── cognition/          # 上下文构建
│       ├── model/              # 模型接口、适配器与便携本地服务管理
│       ├── memory/             # 长期记忆（未实现）
│       ├── capabilities/       # 工具与其他能力（未实现）
│       ├── environment/        # 执行环境（未实现）
│       ├── identity/           # Agent 身份（未实现）
│       ├── relationship/       # 用户关系状态（未实现）
│       ├── state/              # Agent 当前状态（未实现）
│       └── interfaces/         # CLI 等交互入口
├── tests/                      # 模型选择、本地部署及失败路径的自动化测试
├── data/                       # 本地运行数据，不提交 Git
├── workspace/                  # Agent 工作目录，不提交 Git
├── .env.example                # 配置模板
├── pyproject.toml              # Python 项目配置
└── README.md
```

部分目录仍处于接口预留或尚未实现状态。目录存在不代表对应功能已经完成。

## 后续方向与开发记录

长期方向包括独立的持久化记忆、SQLite 存储、记忆提取与检索、上下文注入、Embedding（文本向量化）检索、工具调用循环和受控工作区。Embedding Provider 尚未确定，聊天接口接通不代表向量化接口可用。

本轮 Owner 已确定先做本地对话模型试运行；长期记忆等方向顺延，后续版本范围仍由 Owner 确定。原 Memory 的 `v0.1.Y` 编号仅为候选，已在 Roadmap 改为阶段编号。

| 文档 | 用途与当前状态 |
| --- | --- |
| [AGENTS.md](AGENTS.md) | 项目开发协作规范 |
| [工作日志](docs/work-log.md) | 开发版本、任务记录、历史提交及验证证据 |
| [本地模型](docs/local-model.md) | 安装、运行、实测与回退 |
| [项目流程图 v0.0.5](docs/diagrams/project-flow-v0.0.5.mmd) | 当前实际运行链路与预留模块 |
| [整体架构](docs/architecture.md) | 当前 CLI 架构、目标架构与模块边界（设计草案） |
| [记忆系统设计](docs/memory-system-design.md) | 长期记忆目标与首阶段候选方案（尚未实现） |
| [Roadmap](docs/roadmap.md) | 本轮本地模型计划与后续候选任务 |

本地部署及失败路径的自动化验证：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 开发原则

- LLM 是可替换的认知资源，不能作为长期记忆本身。
- Runtime 负责编排，各子系统负责自己的具体能力。
- Working Memory 与跨重启的长期 Memory 分开管理。
- Model、Memory、Tools 和 Environment 通过稳定接口协作。
- 每个阶段都应形成可以运行、验证和回退的版本。
- 已实现功能、计划功能和预留目录必须明确区分。
