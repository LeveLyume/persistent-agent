from pathlib import Path

from persistent_agent.cognition.context_builder import ContextBuilder
from persistent_agent.config.settings import load_settings
from persistent_agent.model.base import ModelError
from persistent_agent.model.openai_compatible import OpenAICompatibleModel
from persistent_agent.runtime.agent_runtime import AgentRuntime
from persistent_agent.session.working_memory import WorkingMemory


def main() -> None:
    try:
        settings = load_settings(Path.cwd() / ".env")
    except ValueError as error:
        print(f"启动失败：{error}")
        return

    model = OpenAICompatibleModel(
        api_key=settings.api_key,
        base_url=settings.base_url,
        model=settings.model,
    )

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

    print("Persistent Agent 已启动。")
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
    finally:
        model.close()
        print("程序已退出。")


if __name__ == "__main__":
    main()
