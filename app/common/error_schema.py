from typing import Literal

from pydantic import BaseModel, Field

from app.messages import (
    DESCRIPTION_ERROR,
    DESCRIPTION_LOCATION,
    DESCRIPTION_SLUG,
    DESCRIPTION_FIELD,
    DESCRIPTION_CTX,
    DESCRIPTION_DETAILS,
)

ErrorLocation = Literal["query", "path", "body", "header"]

class ErrorDetail(BaseModel):
    message: str = Field(..., description=DESCRIPTION_ERROR)
    location: ErrorLocation | None = Field(None, description=DESCRIPTION_LOCATION)
    slug: str | None = Field(None, description=DESCRIPTION_SLUG)
    field: str | None = Field(None, description=DESCRIPTION_FIELD)
    ctx: dict | None = Field(None, description=DESCRIPTION_CTX)

class ErrorResponse(BaseModel):
    slug: str = Field(..., description=DESCRIPTION_SLUG)
    message: str = Field(..., description=DESCRIPTION_ERROR)
    details: None | list[ErrorDetail] = Field(..., description=DESCRIPTION_DETAILS)