from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Local AI (Ollama) — primary engine
    ollama_url: str = "http://localhost:11434"
    model_local: str = "gemma4:e4b"

    # Anthropic — fallback only (optional)
    anthropic_api_key: str = ""

    # Service URLs (internal ports)
    atlas_url: str = "http://localhost:8000"
    calendar_url: str = "http://localhost:5001"
    connect_url: str = "http://localhost:5000"
    mail_url: str = "http://localhost:8004"
    meet_url: str = "http://localhost:6001"
    writer_url: str = "http://localhost:6011"
    planet_url: str = "http://localhost:46000"
    capital_hub_url: str = "http://localhost:6003"
    secure_url: str = "http://localhost:6004"
    turbotick_url: str = "http://localhost:6100"
    wallet_url: str = "http://localhost:6110"
    dock_url: str = "http://localhost:6120"
    fitterme_url: str = "http://localhost:8000"  # Docker container internal port
    search_url: str = "http://localhost:6200"
    gate_url: str = "http://localhost:45001"
    control_center_url: str = "http://localhost:8077"

    # Gate / Auth
    gate_jwks_url: str = "http://localhost:45001/api/v1/oidc/jwks"

    # Shell config
    orbit_shell_port: int = 6300
    shell_frontend_port: int = 45021
    debug: bool = False

    # Model routing (kept for reference, not used when running local)
    model_simple: str = "claude-haiku-4-5"
    model_standard: str = "claude-sonnet-4-6"
    model_complex: str = "claude-opus-4-6"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
