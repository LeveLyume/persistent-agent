import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_key: str = field(repr=False)
    base_url: str
    model: str


def load_settings(env_path: Path) -> Settings:
    load_dotenv(env_path, encoding="utf-8-sig")

    required = (
        "LLM_API_KEY",
        "LLM_BASE_URL",
        "LLM_MODEL",
    )

    values = {name: os.getenv(name, "").strip() for name in required}

    missing = [name for name, value in values.items() if not value]

    if missing:
        raise ValueError("缺少配置：" + "、".join(missing) + f"。请检查 {env_path}")

    return Settings(
        api_key=values["LLM_API_KEY"],
        base_url=values["LLM_BASE_URL"],
        model=values["LLM_MODEL"],
    )
