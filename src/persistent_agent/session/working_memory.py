from persistent_agent.core.types import Message


class WorkingMemory:
    def __init__(self, max_turns: int = 20) -> None:
        if max_turns < 1:
            raise ValueError("max_turns 必须大于 0。")

        self._messages: list[Message] = []
        self._max_turns = max_turns

    def snapshot(self) -> list[Message]:
        return self._messages.copy()

    def add_turn(self, user_text: str, assistant_text: str) -> None:
        self._messages.extend(
            [
                Message(role="user", content=user_text),
                Message(role="assistant", content=assistant_text),
            ]
        )

        self._messages = self._messages[-self._max_turns * 2 :]

    def clear(self) -> None:
        self._messages.clear()
