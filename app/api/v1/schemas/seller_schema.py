from pydantic import BaseModel, Field, validator
from pydantic.types import StringConstraints
from app.api.common.schemas import ResponseEntity, SchemaType


class SellerBase(SchemaType):
    seller_id: str = Field(..., description="ID único, alfanumérico e lowercase", pattern="^[a-z0-9]+$")
    nome_fantasia: str = Field(..., description="Nome fantasia exclusivo no sistema", min_length=3)
    cnpj: str = Field(..., description="CNPJ com exatamente 14 dígitos numéricos, sem pontuação", min_length=14, max_length=14, pattern=r"^\d{14}$")

class SellerCreate(SellerBase):
    pass

class SellerUpdate(SchemaType):
    nome_fantasia: str
    cnpj: str

class SellerResponse(SellerBase, ResponseEntity):
    pass
