import json

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.common.error_codes import ErrorCodes
from app.common.exceptions import ApplicationException

from .schemas.response import ErrorDetail, get_error_response


async def _get_request_body(request: Request) -> dict | None:
    try:
        return json.loads(await request.body())
    except Exception as ex:
        # XXX Informar que deu erro
        ...
    return None


async def _get_request_info(request: Request) -> dict:
    return {
        "method": request.method,
        "url": request.url,
        "query": request.query_params,
        "content": await _get_request_body(request),
    }


def add_error_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_, exc: HTTPException):
        response = get_error_response(ErrorCodes.SERVER_ERROR.value)
        return JSONResponse(
            status_code=exc.status_code,
            headers=exc.headers,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        errors = exc.errors()
        details: list[ErrorDetail] = []
        for error in errors:
            ctx = error.get("ctx", {})

            details.append(
                ErrorDetail(
                    **{
                        "message": error["msg"],
                        "location": error["loc"][0],
                        "slug": error["type"],
                        "field": ", ".join(map(str, error["loc"][1:])),
                        "ctx": ctx,
                    }
                )
            )

        response = get_error_response(ErrorCodes.UNPROCESSABLE_ENTITY.value, details=details)

        return JSONResponse(
            status_code=ErrorCodes.UNPROCESSABLE_ENTITY.http_code,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(ValidationError)
    async def request_pydantic_validation_error_handler(_: Request, exc: ValidationError) -> JSONResponse:
        errors = exc.errors()
        details: list[ErrorDetail] = []
        for error in errors:
            ctx = error.get("ctx", {})

            if isinstance(ctx.get("error", {}), ValueError):  # pragma: no cover
                # Pydantic não trata direito erros como ValueError, retornando um padrão
                # diferente do FastAPI.
                ctx["error"] = str(ctx["error"])

            details.append(
                ErrorDetail(
                    **{
                        "message": error["msg"],
                        "location": error["loc"][0] if error["loc"] else "body",
                        "slug": error["type"],
                        "field": ", ".join(map(str, error["loc"][1:])) if error["loc"] else "",
                        "ctx": ctx,
                    }
                )
            )

        response = get_error_response(ErrorCodes.UNPROCESSABLE_ENTITY.value, details=details)

        return JSONResponse(
            status_code=ErrorCodes.UNPROCESSABLE_ENTITY.http_code,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(Exception)
    async def default_validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        response = get_error_response(ErrorCodes.SERVER_ERROR.value)
        # XXX Informar que deu erro
        return JSONResponse(
            status_code=ErrorCodes.SERVER_ERROR.http_code,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(ApplicationException)
    async def application_exception_handler(_, exc: ApplicationException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.error_response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )
