# 本地对话模型试运行（v0.1.1）

## 部署与边界

本入口使用 Qwen 官方 `Qwen3-0.6B-Q8_0.gguf`，通过 llama.cpp 的 OpenAI 兼容接口接入现有 CLI、Runtime 和模型适配器。已在 Windows、RTX 5070 Laptop GPU 8 GB、驱动 610.47（CUDA UMD 13.3）上实测。便携部署固定为 Windows x64 CUDA 13.3 构建，不适用于任意操作系统或旧显卡驱动。

部署文件全部位于项目的 `data/local-model/`，该目录已被 Git 忽略。便携程序不安装系统服务、不设置自启动、不修改 PATH、驱动、全局 Python、注册表或防火墙。现有 `.venv` 和 `.env` 保留原样。安装只需要已有的 Python 3.11+，不增加项目 Python 依赖。

| 文件 | 固定来源 | SHA256 |
| --- | --- | --- |
| `llama-b10964-bin-win-cuda-13.3-x64.zip` | [llama.cpp b10964](https://github.com/ggml-org/llama.cpp/releases/tag/b10964) | `cd63ae76ad78a1540aa0f30f6c6284bab14c146d99a58f70c3f0a38cb9c62351` |
| `cudart-llama-bin-win-cuda-13.3-x64.zip` | 同一发布的便携 CUDA DLL | `1462a050eb4c684921ba51dcc4cc488a036674c3e73e9945ee705b854808d03e` |
| `Qwen3-0.6B-Q8_0.gguf` | [Qwen 固定修订 23749fef](https://huggingface.co/Qwen/Qwen3-0.6B-GGUF/tree/23749fefcc72300e3a2ad315e1317431b06b590a) | `9465e63a22add5354d9bb4b99e90117043c7124007664907259bd16d043bb031` |

下载完成后先校验再解压/启用；已有同名文件校验不符时停止并保留文件。失败下载以 `.part` 留在部署目录，重试只重写该临时文件。解压前检查路径，拒绝写出独立运行目录。`manifest.json` 保存来源与校验值；程序和模型均不进入 Git。

## 使用

先按 README 安装项目依赖。以下命令在项目根目录运行。当前电脑已部署；换机或恢复文件时运行一次：

```powershell
.\.venv\Scripts\python.exe -m persistent_agent.interfaces.cli --setup-local
```

日常使用只需要一个 PowerShell 窗口：

```powershell
.\.venv\Scripts\python.exe -m persistent_agent.interfaces.cli
```

启动菜单输入 `1` 选择 DeepSeek，输入 `2` 选择本地 Qwen3-0.6B；输入 `/exit` 可在选择前退出。也可直接指定模型，适合脚本或不想看菜单时使用：

```powershell
.\.venv\Scripts\python.exe -m persistent_agent.interfaces.cli --model local
# 或 --model deepseek
```

选本地时，同一 CLI 从独立文件取得本地密钥，启动 `127.0.0.1:18080` 的 llama.cpp 子进程，等待就绪后进入对话。退出 CLI 时只停止本次启动的子进程。选 DeepSeek 时才读取原 `.env`；本地模式不读取其中的远端密钥。两种模式复用现有模型适配器和 Runtime。

安装时生成随机本地密钥，存于已忽略的 `data/local-model/api-key.txt`，服务和 CLI 共用此文件，不打印密钥。服务仅监听 `127.0.0.1:18080`，限制 CORS 来源，关闭 Web UI，启用离线模式。运行服务期间 API 需要本地密钥；不要将该文件提交或分享。初次下载需要网络，模型推理使用本地文件。

`/reset` 清空会话，`/exit` 退出 CLI。正常退出或在对话中按 Ctrl+C 时，程序会清理自己启动的本地服务并释放模型资源。端口已被其他程序占用时会报告错误，不结束未知进程。服务日志保存在已忽略的 `data/local-model/server.log`。

## 运行参数与限制

- 单会话，4096 Token 上下文，输出上限 512 Token，关闭思考模式。
- 最多 8 个 CPU 工作线程；GPU 层数参数 99，本机日志确认实际 29/29 层加载到 GPU。
- 批大小 256，计算微批大小 128；额外的主机历史提示缓存关闭，避免默认最多 8192 MiB 的缓存预算。
- 温度 0.7、top-p 0.8、top-k 20、min-p 0。采样输出会变化。
- 现有 Working Memory 仍保留最近 20 轮，不等于保证这些消息一定装入 4096 Token。超长请求返回 HTTP 400，可 `/reset` 或缩短输入；没有实现自动 Token 裁剪。
- 达到输出上限时，适配器按既有逻辑显示“回复因长度限制中断，本轮没有保存”。60 秒请求超时、无自动重试仍有效。
- 0.6B 模型用于接入实验。初次测试中曾把“1加1”回答为“1”，后续一次回答正确；这属于回复质量限制，不能把接口测试通过等同于模型能力可靠。
- 内存中的模型提示缓存不属于长期记忆，进程退出后不保留会话。

## 验证记录（2026-09-18）

v0.1.1 的 5 项自动化测试覆盖配置隔离、错误校验文件保留、越界解压拒绝、服务边界参数、HTTP 错误与输出截断不写入会话。v0.1.2 新增模型选择与资源清理测试，当前共 8 项通过。运行：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

本机真实模型验证：健康检查、模型列表、无密钥请求返回 401、CLI 三轮回复与姓名追问、`/reset`、`/exit` 均通过；12063 Token 请求被 4096 Token 限制明确拒绝；停服后的 CLI 显示连接失败并可退出。`.env` 前后 SHA256 相同。

v0.1.2 对统一入口的真实试跑：菜单选择本地 Qwen、姓名追问、`/reset`、`/exit` 均通过；退出后本地端口已关闭，整卡显存由试跑前 2186 MiB 回到 2166 MiB。菜单选择 DeepSeek 可以进入原模式并退出；本次没有向远端 API 发送请求。错误选项会提示重新选择。`.env` 的 SHA256 未改变。

| 实测项 | 本次结果 |
| --- | --- |
| 服务就绪耗时 | 1.110 秒（文件已下载，非冷磁盘基准） |
| 三轮 CLI 整体耗时 | 1.799 秒，包含客户端启动；不作为普遍性能保证 |
| 整卡显存：启动前 / 采样峰值 / 停止后 | 1914 / 3107 / 1909 MiB |
| 日志中的 CUDA 模型缓冲区 / KV 缓冲区 / 计算缓冲区 | 604.15 / 448.00 / 7.50 MiB |

整卡显存每约 0.2 秒采样，也包含桌面与其他程序；不是进程精确峰值。未测试长时间运行、并发、大规模质量评估或 Embedding 共存。原 DeepSeek 真实 API 本次未调用，远端使用路径未修改。

v0.1.1 原始记录保存在已忽略的 `data/local-model/verification.json`、`server.log`；v0.1.2 真实入口测试也已结束。历史显存数字不作为所有运行环境的保证。

## 停止与回退

1. CLI 输入 `/exit` 或在对话中按 Ctrl+C，程序关闭由本次 CLI 启动的服务；不会按进程名批量结束其他服务。
2. 需要回到 DeepSeek 时，再次运行统一入口选 `1`，或使用 `--model deepseek`。无需恢复配置或重装依赖。
3. 需要卸载便携部署时，先确认本项目服务已停止，再删除**本项目的 `data/local-model/` 目录**。该目录包含本地密钥、下载包、运行库、模型与测试记录；不要删除整个 `data/`。
4. 需要撤销仓库接入时，对本任务提交做单独的 Git revert 并复查；保留其他任务的改动，不使用 `reset --hard` 或强制推送。

如果启动提示端口占用，先检查占用来源，不结束未知进程；如果缺少驱动或 DLL，保留错误信息排查，不自动更换系统驱动。中断部署后原远端 CLI 仍可使用。
