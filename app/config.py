from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "amzn-stock-agent"
    app_env: str = "dev"
    log_level: str = "INFO"

    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    langfuse_public_key: str | None = None
    langfuse_secret_key: str | None = None
    langfuse_base_url: str = "https://cloud.langfuse.com"

    vector_store_path: str = "./data/vectorstore"
    docs_path: str = "./data/docs"

    default_ticker: str = "AMZN"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()