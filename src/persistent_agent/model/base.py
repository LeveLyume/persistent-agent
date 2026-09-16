from typing import Protocol, Sequence

from persistent_agent.core.types import Message


class ModelProvider(Protocol):
    def generate(self, messages: Sequence[Message]) -> str: ...


class ModelError(Exception):
    """模型调用失败时，对外提供的统一异常。"""
