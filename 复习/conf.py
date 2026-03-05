import os
from pydantic_settings import BaseSettings,SettingsConfigDict
PATH = os.path.abspath("__file__")


class Settings(BaseSettings):
    deepseek_api_key : str
    deepseek_base_url : str
    deepseek_chat_model : str
    deepseek_reasoner_model : str
    openweather_api_key : str


    model_config = SettingsConfigDict(
        env_file =  ".env",
        env_file_encoding = "utf-8",
        case_sensitive = True,

    )

settings = Settings()

if __name__ == '__main__':
    print(settings.deepseek_base_url)