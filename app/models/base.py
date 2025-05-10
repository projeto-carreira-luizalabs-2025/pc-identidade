from datetime import datetime
from uuid import UUID as UuidType

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter
from uuid_extensions import uuid7

from app.common.datetime import utcnow


class UuidModel(BaseModel):
    id: UuidType = Field(default_factory=uuid7, alias="_id")


class AuditModel(BaseModel):
    created_at: datetime = Field(default_factory=utcnow, description="Data e hora da criação")
    updated_at: datetime | None = Field(None, description="Data e hora da atualização")
    created_by: str | None = Field(None, description="Criado por")
    updated_by: str | None = Field(None, description="Atualizado por")

    audit_created_at: datetime | None = Field(None, description="Data e hora da efetiva criação do registro")
    audit_updated_at: datetime | None = Field(None, description="Data e hora da efetiva atualização do registro")


class PersistableEntity(UuidModel, AuditModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @classmethod
    def from_json(cls, json_data: str):
        return TypeAdapter(cls).validate_json(json_data)
