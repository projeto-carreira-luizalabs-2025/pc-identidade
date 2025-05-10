from app.api.common.schemas import ResponseEntity, SchemaType


class CustomerSchema(SchemaType):
    name: str
    email: str


class CustomerResponse(CustomerSchema, ResponseEntity):
    """Resposta adicionando os campos de auditoria e id do objeto"""


class CustomerCreate(CustomerSchema):
    """Schema para criação customers"""


class CustomerUpdate(SchemaType):
    """Permite apenas a atualização do nome"""

    name: str
