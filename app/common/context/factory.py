from contextvars import ContextVar

from app.common.exceptions import ForbiddenException

from .model import AppContext

_app_context: ContextVar[AppContext | None] = ContextVar("_app_context", default=None)


def set_context(context: AppContext):
    _app_context.set(context)


def get_context() -> AppContext:  # pragma: no cover
    if context := _app_context.get():
        return context

    raise ForbiddenException()
