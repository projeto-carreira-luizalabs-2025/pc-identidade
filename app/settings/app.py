from pydantic import Field, MongoDsn
from pydantic_settings import SettingsConfigDict

from .base import BaseSettings


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", case_sensitive=False)
    version: str = "0.0.2"
    app_version: str = Field("0.0.1", description="Versão da aplicação")
    app_name: str = Field(default="PC Identidade", title="Nome da aplicação")
    memory_min: int = Field(default=64, title="Limite mínimo de memória disponível em MB")
    disk_usage_max: int = Field(default=80, title="Limite máximo de 80% de uso de disco")
    app_db_url_mongo: str = Field(..., title="URI para o MongoDB")
    MONGO_DB: str = Field(..., title="Nome do banco de dados padrão")

    KEYCLOAK_URL: str = Field(..., description="URL base do Keycloak")
    KEYCLOAK_REALM_NAME: str = Field(..., description="Nome do Realm no Keycloak")
    KEYCLOAK_CLIENT_ID: str = Field(..., description="Client ID da aplicação no Keycloak")

    KEYCLOAK_WELL_KNOWN_URL: str = Field(..., description="URL .well-known do OpenID Connect do Keycloak")

    KEYCLOAK_ADMIN_USER: str = Field(..., description="Usuário admin do Keycloak")
    KEYCLOAK_ADMIN_PASSWORD: str = Field(..., description="Senha do usuário admin do Keycloak")
    KEYCLOAK_ADMIN_CLIENT_ID: str = Field(..., description="Client ID para operações de admin")

    pc_logging_level: str = Field("INFO", description="Nível do logging")
    pc_logging_env: str = Field("prod", description="Ambiente do logging (dev ou prod)")
    
    # Gemini AI
    API_KEY_GEMINI: str = Field(..., description="API Key do Google Gemini")
    
    # Webhook Configuration
    WEBHOOK_URL: str = Field(..., description="URL do webhook para envio de notificações")


settings = AppSettings()
