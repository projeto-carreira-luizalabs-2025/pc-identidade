from dotenv import load_dotenv
load_dotenv()

from enum import StrEnum
from os import environ
from typing import Tuple, Type

from pydantic import Field
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import PydanticBaseSettingsSource, SettingsConfigDict

ENV = environ.get("ENV", "missing environment")
# Os arquivos padrão de configurações por ambiente são carregados de acordo com a variável ENV.
# Se uma variável for sobrescrita no arquivo .env local ela terá precedência sobre os arquivos dotenv.dev|test|prod
# As variáveis de ambiente do SO tem prioridade em relação ao que está gravado nos arquivos
ENV_FILES = {"dev": "dotenv.dev", "prod": "dotenv.prod", "test": "dotenv.test"}


class EnvironmentEnum(StrEnum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"
    TEST = "test"

    @property
    def is_test(self):
        return self == EnvironmentEnum.TEST

    @property
    def is_production(self):
        return self == EnvironmentEnum.PRODUCTION

    @property
    def is_development(self):
        return self == EnvironmentEnum.DEVELOPMENT


if ENV not in EnvironmentEnum:
    raise ValueError("ENV must be either 'dev', 'prod' or 'test'")  # pragma: no cover

ENV_FILE = f"devtools/{ENV_FILES[ENV]}"


class BaseSettings(PydanticBaseSettings):
    env: EnvironmentEnum = Field(default=EnvironmentEnum.DEVELOPMENT, title="Ambiente da aplicação")
    env_file: str = ENV_FILE

    model_config = SettingsConfigDict(
        env_file=[ENV_FILE, ".env"],
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        validate_default=True,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[PydanticBaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """Change source priority order (env trumps environment)."""
        return (init_settings, env_settings, dotenv_settings, file_secret_settings)
