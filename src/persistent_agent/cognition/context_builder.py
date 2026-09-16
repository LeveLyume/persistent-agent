from typing import Sequence

from persistent_agent.core.types import Message


class ContextBuilder:
    def __init__(self, system_prompt: str) -> None:
        self._system_prompt = system_prompt

    def build(
        self,
        history: Sequence[Message],
        user_text: str,
    ) -> list[Message]:
        return [
            Message(role="system", content=self._system_prompt),
            *history,
            Message(role="user", content=user_text),
        ]
