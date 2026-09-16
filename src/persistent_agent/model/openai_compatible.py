from typing import Sequence

from openai import (
    OpenAI,
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)

from persistent_agent.core.types import Message
from persistent_agent.model.base import ModelError


class OpenAICompatibleModel:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
    ) -> None:
        self._model = model
        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=60.0,
            max_retries=0,
        )

    def generate(self, messages: Sequence[Message]) -> str:
        payload = [
            {"role": message.role, "content": message.content} for message in messages
        ]

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=payload,
            )
        except AuthenticationError:
            raise ModelError("身份验证失败，请检查 API Key。") from None
        except RateLimitError:
            raise ModelError("请求受到限制，请稍后再试。") from None
        except APITimeoutError:
            raise ModelError("模型响应超时，请稍后再试。") from None
        except APIConnectionError:
            raise ModelError("无法连接模型服务，请检查网络和 API 地址。") from None
        except APIStatusError as error:
            raise ModelError(
                f"模型服务返回 HTTP {error.status_code}，"
                "请检查模型配置或平台账户状态。"
            ) from None

        if not response.choices:
            raise ModelError("模型没有返回候选回复。")

        choice = response.choices[0]
        content = choice.message.content

        if choice.finish_reason == "length":
            raise ModelError("回复因长度限制中断，本轮没有保存。")

        if not content or not content.strip():
            raise ModelError("模型没有返回文字内容。")

        return content

    def close(self) -> None:
        self._client.close()
