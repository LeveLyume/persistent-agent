# Persistent Agent

一个面向长期运行和持续扩展的 Agent 项目。

项目将 Runtime、模型、会话、长期记忆、工具和执行环境划分为独立模块，并为 Identity、Relationship、State 等角色连续性能力保留扩展空间。

## 当前状态

项目目前处于早期开发阶段，已经实现：

- 基于 CLI（命令行界面）的连续对话
- 通过 OpenAI 兼容接口调用 DeepSeek
- 当前会话历史记录
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
- Web 或桌面界面

> 当前的 Working Memory 只存在于程序内存中。关闭程序或执行 `/reset` 后，会话历史会丢失。

## 架构概览

当前已经跑通的调用链路：

```text
CLI
 ↓
Agent Runtime
 ↓
Context Builder
 ↓
Working Memory
 ↓
Model Provider
 ↓
DeepSeek API
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
- DeepSeek API Key
- Windows PowerShell（以下命令以 Windows 为例）

当前开发环境使用 Python 3.13.7。

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

## 配置

复制配置模板：

```powershell
Copy-Item .env.example .env
```

打开项目根目录中的 `.env`，填写：

```dotenv
LLM_API_KEY=你的DeepSeek_API_Key
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-flash
```

真实 API Key 只能保存在本地 `.env` 中。

不要将 API Key 写进：

- `README.md`
- `.env.example`
- 源代码
- Git 提交记录

`.env` 已通过 `.gitignore` 排除，不应上传到 GitHub。

## 运行

确保 PowerShell 当前位于项目根目录，然后执行：

```powershell
.\.venv\Scripts\python.exe -m persistent_agent.interfaces.cli
```

程序启动后可以直接输入消息：

```text
你：我叫 LeveLyume，正在学习计算机。
Agent：……
```

继续询问时，程序会把当前会话历史一起发送给模型：

```text
你：我叫什么？正在学什么？
Agent：……
```

## CLI 命令

| 命令     | 作用             |
| -------- | ---------------- |
| `/reset` | 清空当前会话历史 |
| `/exit`  | 退出程序         |

`/reset` 当前只清空内存中的会话记录。长期记忆系统完成后，它仍不会删除长期记忆。

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
│       ├── model/              # 模型接口与适配器
│       ├── memory/             # 长期记忆系统
│       ├── capabilities/       # 工具与其他能力
│       ├── environment/        # 执行环境
│       ├── identity/           # Agent 身份
│       ├── relationship/       # 用户关系状态
│       ├── state/              # Agent 当前状态
│       └── interfaces/         # CLI 等交互入口
├── tests/                      # 单元测试与集成测试
├── data/                       # 本地运行数据，不提交 Git
├── workspace/                  # Agent 工作目录，不提交 Git
├── .env.example                # 配置模板
├── pyproject.toml              # Python 项目配置
└── README.md
```

部分目录仍处于接口预留或尚未实现状态。目录存在不代表对应功能已经完成。

## V0.1 路线

- [x] 创建项目结构
- [x] 建立 Python 虚拟环境
- [x] 接通 DeepSeek API
- [x] 实现 CLI 连续对话
- [x] 实现 Working Memory
- [x] 实现基础 Context Builder
- [ ] 定义长期记忆数据结构
- [ ] 使用 SQLite 持久化记忆
- [ ] 实现记忆保存、读取与删除
- [ ] 实现记忆检索与上下文注入
- [ ] 接入 Embedding 语义检索
- [ ] 实现基础工具注册与调用循环
- [ ] 限制工具只能访问指定工作区
- [ ] 完成 V0.1 集成验证

## 设计文档

| 文档                           | 内容                         |
| ------------------------------ | ---------------------------- |
| `docs/architecture.md`         | 整体架构和模块边界           |
| `docs/memory-system-design.md` | 长期记忆系统设计             |
| `docs/roadmap.md`              | 项目演进路线                 |
| `docs/work-log.md`             | 实际开发过程、问题和交接记录 |

## 开发原则

- LLM 是可替换的认知资源，不能作为长期记忆本身。
- Runtime 负责编排，各子系统负责自己的具体能力。
- Working Memory 与跨重启的长期 Memory 分开管理。
- Model、Memory、Tools 和 Environment 通过稳定接口协作。
- 每个阶段都应形成可以运行、验证和回退的版本。
- 已实现功能、计划功能和预留目录必须明确区分。
