from datetime import datetime
from uuid import UUID as UuidType

from pydantic import BaseModel as SchemaType
from pydantic import ConfigDict, Field


class UuidSchema(SchemaType):
    id: UuidType | None = Field(None, description="Id único do objeto")


class OwnershipSchema(SchemaType):
    tenant_id: str = Field(..., description="Código do tenant ao qual pertence o item")


class AuditSchema(SchemaType):
    created_at: datetime = Field(..., description="Data e hora da criação")
    updated_at: datetime | None = Field(None, description="Data e hora da atualização")
    created_by: str = Field(..., description="Criado por")
    updated_by: str | None = Field(None, description="Atualizado por")


class ResponseEntity(AuditSchema, UuidSchema, OwnershipSchema):

    model_config = ConfigDict(from_attributes=True)
