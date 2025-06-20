from typing import Generic, Literal, Sequence, TypeVar

from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.common.error_codes import ErrorInfo
from app.settings import api_settings

from .navigation_links import NavigationLinks

T = TypeVar("T")

PAGE_MAX_LIMIT = api_settings.pagination.max_limit

DESCRIPTION_ERROR = "Descrição do erro"


class PageResponse(BaseModel):
    limit: int | None = Field(
        default=50,
        ge=1,
        le=PAGE_MAX_LIMIT,
        description="Retorna a quantidade específica de registros se houver.",
    )
    offset: int | None = Field(
        default=0,
        ge=0,
        description=("Posição do registro de referência, a partir dele serão retornados os próximos N registros."),
    )
    count: int | None = Field(default=0, description="Quantidade de registros que foi retornada nessa página.")
    max_limit: int | None = Field(
        default=PAGE_MAX_LIMIT,
        description="Refere-se ao valor máximo que pode ser utilizado no campo limit.",
    )


class Page(BaseModel):
    current: int | None = Field(1, description="Current page")
    previous: int | None = Field(None, description="Previous page")
    next: int | None = Field(None, description="Next page")
    size: int = Field(20, description="Number of items per page")
    pages: int = Field(..., description="Total of pages")


class ListMeta(BaseModel):
    page: PageResponse | None = Field(default=None, description="Pagination metadata")
    links: NavigationLinks | None = Field(default=None, description="Navigation metadata")


class ListResponse(BaseModel, Generic[T]):
    meta: ListMeta | None = Field(None, description="Metadata of the response")
    results: Sequence[T] | None = Field(None, description="The content of the response")


ErrorLocation = Literal["query", "path", "body", "header"]  # type: ignore[valid-type]


class ErrorDetail(BaseModel):
    message: str = Field(..., description=DESCRIPTION_ERROR)
    location: ErrorLocation | None = Field(None, description=DESCRIPTION_ERROR)
    slug: str | None = Field(None, description="Identificação do erro")
    field: str | None = Field(None, description="Campo que gerou o erro")
    ctx: dict | None = Field(None, description="Contexto do erro")


class ErrorResponse(BaseModel):
    slug: str = Field(..., description="Identificação do erro")
    message: str = Field(..., description=DESCRIPTION_ERROR)
    details: None | list[ErrorDetail] = Field(..., description="Detalhes do erro")


class FileBinaryResponse(Response):
    media_type = "binary/octet-stream"


def get_list_response(
    page: PageResponse,
    links: NavigationLinks,
    results: Sequence[BaseModel] | None = None,
) -> ListResponse:
    meta_kwargs: dict[str, PageResponse | NavigationLinks] = {
        "page": page,
        "links": links,
    }
    kwargs: dict[str, Sequence[BaseModel] | ListMeta | None] = {
        "results": results,
        "meta": ListMeta(**meta_kwargs),
    }

    return ListResponse(**kwargs)


def get_error_response(error: ErrorInfo, details: list[ErrorDetail] | None = None) -> ErrorResponse:
    return ErrorResponse(slug=error.slug, message=error.message, details=details)
