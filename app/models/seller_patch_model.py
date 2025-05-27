from typing import Optional
from pydantic import BaseModel, Field, validator


class SellerPatch(BaseModel):
    nome_fantasia: Optional[str] = Field(None, description="Nome fantasia exclusivo no sistema")
    cnpj: Optional[str] = Field(None, description="CNPJ com exatamente 14 dígitos numéricos, sem pontuação")

    @validator("nome_fantasia")
    def validar_nome_fantasia(cls, v):
        if v is not None and len(v.strip()) < 3:
            raise ValueError("O nome_fantasia deve conter ao menos 3 caracteres.")
        return v

    @validator("cnpj")
    def validar_cnpj(cls, v):
        if v is not None and (not v.isdigit() or len(v) != 14):
            raise ValueError("O CNPJ deve conter exatamente 14 dígitos numéricos.")
        return v
