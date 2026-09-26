from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "Company Brain"
    APP_VERSION: str = "0.1.0"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "company_brain"
    POSTGRES_USER: str = "company_brain"
    POSTGRES_PASSWORD: str = "company_brain_dev"

    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "company_brain_dev"

    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file="../.env",
        extra="ignore"
    )

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )


settings = Settings()
