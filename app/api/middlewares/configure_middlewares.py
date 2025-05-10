from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api.common.trace import get_trace_id

from ...settings import ApiSettings

HEADER_X_REQUEST_ID = "X-Request-ID"


def configure_middlewares(app: FastAPI, settings: ApiSettings) -> None:
    app.add_middleware(
        CORSMiddleware,  # type: ignore[attr-defined]
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[HEADER_X_REQUEST_ID],
    )
    app.add_middleware(
        CorrelationIdMiddleware,
        header_name=HEADER_X_REQUEST_ID,
        update_request_header=True,
        generator=lambda: get_trace_id(),
    )
    
    app.add_middleware(GZipMiddleware, minimum_size=1000)
