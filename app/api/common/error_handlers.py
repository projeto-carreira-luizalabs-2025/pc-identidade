from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from .schemas.response import ErrorDetail, get_error_response
from app.common.error_codes import ErrorCodes

VALID_LOCATIONS = {"query", "path", "body", "header"}

def extract_error_detail(error):
    ctx = error.get("ctx", {})
    if isinstance(ctx.get("error", {}), ValueError):
        ctx["error"] = str(ctx["error"])
    raw_location = error["loc"][0] if error["loc"] else "body"
    location = raw_location if raw_location in VALID_LOCATIONS else "body"
    return ErrorDetail(
        message=error["msg"],
        location=location,
        slug=error["type"],
        field=", ".join(map(str, error["loc"][1:])) if len(error["loc"]) > 1 else "",
        ctx=ctx,
    )

def extract_error_detail_body(error):
    ctx = error.get("ctx", {})
    if isinstance(ctx.get("error", {}), ValueError):
        ctx["error"] = str(ctx["error"])
    return ErrorDetail(
        message=error["msg"],
        location="body",
        slug=error["type"],
        field=", ".join(map(str, error["loc"][1:])) if error["loc"] else "",
        ctx=ctx,
    )

def add_error_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_, exc: HTTPException):
        response = get_error_response(ErrorCodes.SERVER_ERROR.value)
        return JSONResponse(
            status_code=exc.status_code,
            headers=exc.headers,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(ValidationError)
    async def request_pydantic_validation_error_handler(_: Request, exc: ValidationError) -> JSONResponse:
        errors = exc.errors()
        details = [extract_error_detail(error) for error in errors]
        response = get_error_response(ErrorCodes.UNPROCESSABLE_ENTITY.value, details=details)
        return JSONResponse(
            status_code=ErrorCodes.UNPROCESSABLE_ENTITY.http_code,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(ValidationError)
    async def request_pydantic_validation_error_handler_body(_: Request, exc: ValidationError) -> JSONResponse:
        errors = exc.errors()
        details = [extract_error_detail_body(error) for error in errors]
        response = get_error_response(ErrorCodes.UNPROCESSABLE_ENTITY.value, details=details)
        return JSONResponse(
            status_code=ErrorCodes.UNPROCESSABLE_ENTITY.http_code,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )