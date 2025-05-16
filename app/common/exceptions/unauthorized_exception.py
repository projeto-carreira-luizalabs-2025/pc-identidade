from typing import TYPE_CHECKING

from app.common.error_codes import ErrorCodes

from . import ApplicationException

if TYPE_CHECKING:
    from app.api.common.schemas.response import ErrorDetail


class UnauthorizedException(ApplicationException):
    def __init__(
        self,
        details: list["ErrorDetail"] | None = None,
        message: str | None = None,
    ):
        super().__init__(error_info=ErrorCodes.UNAUTHORIZED.value, details=details, message=message)
