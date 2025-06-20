import re
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator

from app.api.common.schemas import SchemaType
from app.messages import (
    DESC_SELLER_ID,
    DESC_NOME_FANTASIA,
    DESC_CNPJ,
    MSG_SELLER_ID_OBRIGATORIO,
    MSG_SELLER_ID_FORMATO,
    MSG_NOME_FANTASIA_CURTO,
    MSG_CNPJ_FORMATO,
    MSG_CNPJ_FORMATO_REPLACE,
)

class SellerBase(SchemaType):
    seller_id: str = Field(..., description=DESC_SELLER_ID)
    nome_fantasia: str = Field(..., description=DESC_NOME_FANTASIA)
    cnpj: str = Field(..., description=DESC_CNPJ)

    @validator('seller_id')
    def validar_seller_id(cls, v):
        if not v:
            raise ValueError(MSG_SELLER_ID_OBRIGATORIO)
        if not re.fullmatch(r"^[a-z0-9]+$", v):
            raise ValueError(MSG_SELLER_ID_FORMATO)
        return v
    
    @validator('nome_fantasia')
    def validar_nome_fantasia(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError(MSG_NOME_FANTASIA_CURTO)
        return v

    @validator('cnpj')
    def validar_cnpj(cls, v):
        if not v or not v.isdigit() or len(v) != 14:
            raise ValueError(MSG_CNPJ_FORMATO)
        return v


class SellerCreate(SellerBase):
    pass


class SellerUpdate(SchemaType):
    nome_fantasia: Optional[str] = Field(None, description=DESC_NOME_FANTASIA)
    cnpj: Optional[str] = Field(None, description=DESC_CNPJ)

    @validator('nome_fantasia')
    def validar_nome_fantasia(cls, v):
        if v is not None and len(v.strip()) < 3:
            raise ValueError(MSG_NOME_FANTASIA_CURTO)
        return v

    @validator('cnpj')
    def validar_cnpj(cls, v):
        if v is not None and (not v.isdigit() or len(v) != 14):
            raise ValueError(MSG_CNPJ_FORMATO)
        return v


class SellerReplace(SchemaType):
    nome_fantasia: str = Field(..., description=DESC_NOME_FANTASIA)
    cnpj: str = Field(..., description=DESC_CNPJ)

    @validator("nome_fantasia")
    def validar_nome_fantasia(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError(MSG_NOME_FANTASIA_CURTO)
        return v

    @validator("cnpj")
    def validar_cnpj(cls, v):
        if not v.isdigit() or len(v) != 14:
            raise ValueError(MSG_CNPJ_FORMATO_REPLACE)
        return v


class SellerResponse(SellerBase):
    pass