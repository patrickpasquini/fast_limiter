from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, RedisDsn


class EnvSettings(BaseSettings):
    redis_url: RedisDsn = Field("redis://localhost", validation_alias="REDIS_URL")
    db_path: str = Field("rtl.db", validation_alias="DB_PATH")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


env_settings = EnvSettings()
