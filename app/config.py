from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    cors_origins: str
    supabase_key: str

    model_config = SettingsConfigDict(

         env_file = ".envi",
         env_file_encoding="utf-8"
    )

settings = Settings()
