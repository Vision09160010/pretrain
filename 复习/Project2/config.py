from pydantic_settings import BaseSettings,SettingsConfigDict
import os
PATH = os.path.abspath(os.path.dirname(__file__))

class Settings(BaseSettings):
    base_url: str
    api_key: str
    model_name: str

    model_config = SettingsConfigDict(
        env_file = PATH + "/.env",
        case_sensitive = False
    )

settings = Settings()

if __name__ == '__main__':
    print(settings.api_key)
    print(settings.model_name)
    print(settings.base_url)