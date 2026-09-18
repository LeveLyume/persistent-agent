import argparse
from contextlib import ExitStack
from pathlib import Path
import zipfile

from persistent_agent.cognition.context_builder import ContextBuilder
from persistent_agent.config.settings import load_settings
from persistent_agent.model.base import ModelError
from persistent_agent.model.local_model import LocalModelServer, local_settings, setup
from persistent_agent.model.openai_compatible import OpenAICompatibleModel
from persistent_agent.runtime.agent_runtime import AgentRuntime
from persistent_agent.session.working_memory import WorkingMemory


def main() -> None:
    parser = argparse.ArgumentParser(description="Persistent Agent 对话入口")
    parser.add_argument("--model", choices=("deepseek", "local"), help="跳过交互式模型选择")
    parser.add_argument("--setup-local", action="store_true", help="下载并校验本地模型与便携服务")
    args = parser.parse_args()

    if args.setup_local:
        try:
            setup()
        except (OSError, ValueError, zipfile.BadZipFile) as error:
            print(f"本地模型部署失败：{error}")
        return

    choice = args.model
    while choice is None:
        try:
            answer = input("选择模型：1 DeepSeek；2 本地 Qwen3-0.6B；/exit 退出\n> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n对话已中止。")
            return
        if answer in ("1", "deepseek"):
            choice = "deepseek"
        elif answer in ("2", "local"):
            choice = "local"
        elif answer == "/exit":
            return
        else:
            print("请选择 1、2 或 /exit。")

    try:
        settings = local_settings() if choice == "local" else load_settings(Path.cwd() / ".env")
    except (OSError, ValueError) as error:
        print(f"启动失败：{error}")
        return
    try:
        with ExitStack() as stack:
            if choice == "local":
                print("正在启动本地 Qwen3-0.6B……")
                stack.enter_context(LocalModelServer())
            model = OpenAICompatibleModel(
                api_key=settings.api_key,
                base_url=settings.base_url,
                model=settings.model,
            )
            stack.callback(model.close)
            runtime = AgentRuntime(
                model=model,
                memory=WorkingMemory(max_turns=20),
                context_builder=ContextBuilder(
                    system_prompt=(
                        "你是 Persistent Agent，一个正在开发中的 AI 助手。"
                        "默认使用中文回答。"
                        "准确说明自己的能力，不编造经历或记忆。"
                        "目前只能参考本次会话提供的历史，尚无长期记忆和工具能力。"
                    )
                ),
            )
            print(f"Persistent Agent 已启动，当前模型：{choice}。")
            print("输入 /exit 退出，输入 /reset 清空当前会话。")
            try:
                while True:
                    user_text = input("\n你：").strip()
                    if not user_text:
                        continue
                    if user_text == "/exit":
                        break
                    if user_text == "/reset":
                        runtime.reset_session()
                        print("当前会话已清空。")
                        continue
                    print("正在等待模型回复……")
                    try:
                        reply = runtime.handle_message(user_text)
                    except ModelError as error:
                        print(f"请求失败：{error}")
                        continue
                    print(f"\nAgent：{reply}")
            except (KeyboardInterrupt, EOFError):
                print("\n对话已中止。")
        print("程序已退出。")
    except (OSError, ValueError, RuntimeError) as error:
        print(f"启动失败：{error}")


if __name__ == "__main__":
    main()
