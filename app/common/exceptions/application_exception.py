from typing import TYPE_CHECKING

from fastapi import HTTPException

from app.api.common.schemas.response import ErrorResponse
from app.common.error_codes import ErrorInfo

if TYPE_CHECKING:
    from app.api.common.schemas.response import ErrorDetail


class ApplicationException(HTTPException):
    def __init__(
        self,
        error_info: ErrorInfo,
        details: list["ErrorDetail"] | None = None,
        message: str | None = None
    ):
        self.slug = error_info.slug
        self.message = message or error_info.message 
        self.status_code = error_info.http_code
        self.details = details

    @property
    def error_response(self):
        return ErrorResponse(slug=self.slug, message=self.message, details=self.details)
