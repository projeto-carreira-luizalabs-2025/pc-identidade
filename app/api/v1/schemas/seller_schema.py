import re
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.api.common.schemas import SchemaType


class SellerBase(SchemaType):
    seller_id: str = Field(..., description="ID único, alfanumérico e lowercase")
    nome_fantasia: str = Field(..., description="Nome fantasia exclusivo no sistema")
    cnpj: str = Field(..., description="CNPJ com exatamente 14 dígitos numéricos, sem pontuação")

    @validator('seller_id')
    def validar_seller_id(cls, v):
        if not v:
            raise ValueError("O seller_id é obrigatório.")
        if not re.fullmatch(r"^[a-z0-9]+$", v):
            raise ValueError(
                "O seller_id deve conter apenas letras minúsculas e números, sem espaços ou caracteres especiais."
            )
        return v

    @validator('nome_fantasia')
    def validar_nome_fantasia(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError("O nome_fantasia deve conter ao menos 3 caracteres.")
        return v

    @validator('cnpj')
    def validar_cnpj(cls, v):
        if not v or not v.isdigit() or len(v) != 14:
            raise ValueError("O CNPJ deve conter exatamente 14 dígitos numéricos, sem pontuação.")
        return v


class SellerCreate(SellerBase):
    pass


class SellerUpdate(SchemaType):
    nome_fantasia: Optional[str] = Field(None, description="Nome fantasia exclusivo no sistema")
    cnpj: Optional[str] = Field(None, description="CNPJ com exatamente 14 dígitos numéricos, sem pontuação")

    @validator('nome_fantasia')
    def validar_nome_fantasia(cls, v):
        if v is not None and len(v.strip()) < 3:
            raise ValueError("O nome_fantasia deve conter ao menos 3 caracteres.")
        return v

    @validator('cnpj')
    def validar_cnpj(cls, v):
        if v is not None and (not v.isdigit() or len(v) != 14):
            raise ValueError("O CNPJ deve conter exatamente 14 dígitos numéricos, sem pontuação.")
        return v


class SellerResponse(SellerBase):
    pass
