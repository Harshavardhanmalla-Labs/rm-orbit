import os
from dataclasses import dataclass


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


@dataclass(frozen=True)
class LLMSettings:
    provider: str
    model: str
    base_url: str
    api_key: str
    timeout_seconds: float
    max_retries: int
    json_repair_attempts: int

    @property
    def is_ollama(self) -> bool:
        return self.provider == "ollama"


def get_llm_settings() -> LLMSettings:
    provider = _env("RESEARCH_LLM_PROVIDER", "ollama").lower()
    model = _env("RESEARCH_LLM_MODEL", "gemma4:e4b")

    default_base_url = "http://localhost:11434/v1" if provider == "ollama" else ""
    default_api_key = "ollama" if provider == "ollama" else ""

    return LLMSettings(
        provider=provider,
        model=model,
        base_url=_env("RESEARCH_LLM_BASE_URL", default_base_url),
        api_key=_env("RESEARCH_LLM_API_KEY", default_api_key),
        timeout_seconds=float(_env("RESEARCH_LLM_TIMEOUT_SECONDS", "180")),
        max_retries=int(_env("RESEARCH_LLM_MAX_RETRIES", "2")),
        json_repair_attempts=int(_env("RESEARCH_LLM_JSON_REPAIR_ATTEMPTS", "3")),
    )
