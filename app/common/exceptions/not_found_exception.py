from typing import TYPE_CHECKING

from app.common.error_codes import ErrorCodes

from . import ApplicationException

if TYPE_CHECKING:
    from app.api.common.schemas.response import ErrorDetail


class NotFoundException(ApplicationException):
    def __init__(
        self,
        message: str | None = None,
        details: list["ErrorDetail"] | None = None
    ):
        super().__init__(
            error_info=ErrorCodes.NOT_FOUND.value,
            message=message,
            details=details
        )
