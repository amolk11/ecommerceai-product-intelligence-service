from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "product-intelligence-service"
    app_version: str = "0.1.0"
    environment: str = "local"

    db_url: str | None = None
    
    cache_enabled: bool = True

    redis_host: str = "localhost"
    redis_port: int = 6379
    cache_ttl: int = 3600

    startup_validation_enabled: bool = True

    log_level: str = "INFO"
    log_dir: str = "logs"
    log_to_console: bool = True
    log_to_file: bool = True
    log_file_max_bytes: int = 10 * 1024 * 1024
    log_file_backup_count: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def is_test(self) -> bool:
        return self.environment.lower() == "test"

    @property
    def should_validate_infrastructure(self) -> bool:
        return self.startup_validation_enabled and not self.is_test


settings = Settings()
