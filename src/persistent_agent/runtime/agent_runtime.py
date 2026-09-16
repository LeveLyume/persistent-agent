from persistent_agent.cognition.context_builder import ContextBuilder
from persistent_agent.model.base import ModelProvider
from persistent_agent.session.working_memory import WorkingMemory


class AgentRuntime:
    def __init__(
        self,
        model: ModelProvider,
        memory: WorkingMemory,
        context_builder: ContextBuilder,
    ) -> None:
        self._model = model
        self._memory = memory
        self._context_builder = context_builder

    def handle_message(self, user_text: str) -> str:
        messages = self._context_builder.build(
            history=self._memory.snapshot(),
            user_text=user_text,
        )

        reply = self._model.generate(messages)
        self._memory.add_turn(user_text, reply)

        return reply

    def reset_session(self) -> None:
        self._memory.clear()
