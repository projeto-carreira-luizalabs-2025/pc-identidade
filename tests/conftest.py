from app.api.router import routes as router
from app.api.api_application import create_app
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import APIRouter, FastAPI
from app.settings import ApiSettings, api_settings
from app.container import Container
from dependency_injector.wiring import providers
from fastapi.testclient import TestClient

@pytest.fixture
def mock_mongo_client():
    client = MagicMock()
    collection = MagicMock()

    collection.insert_one = AsyncMock()
    collection.find_one = AsyncMock()
    collection.find_one_and_update = AsyncMock()
    collection.delete_one = AsyncMock()

    class AsyncCursor:
        def __init__(self, docs):
            self.docs = docs

        def skip(self, n):
            return self

        def limit(self, n):
            return self

        def sort(self, *args, **kwargs):
            return self

        def __aiter__(self):
            async def gen():
                for doc in self.docs:
                    yield doc
            return gen()

    collection.find.return_value = AsyncCursor([])

    # Corrigido aqui: adiciona a chave 'sellers' ao dicionário
    client.get_default_database.return_value = {
        "test_collection": collection,
        "sellers": collection,
    }

    return client, collection


@pytest.fixture
def dummy_router():
    router = APIRouter()

    @router.get("/dummy")
    async def dummy_route():
        return {"message": "ok"}

    return router


@pytest.fixture
def dummy_settings():
    return ApiSettings(
        app_name="TestApp",
        openapi_path="/openapi.json",
        version="0.1.0",
        health_check_base_path="/health"
    )

@pytest.fixture
def mock_seller_service():
    return AsyncMock()


@pytest.fixture
def client(mock_seller_service):
    from app.container import Container
    from app.api.v1.routers import seller_router

    app = FastAPI()

    container = Container()
    container.seller_service.override(providers.Object(mock_seller_service))

    container.wire(modules=[seller_router])
    app.container = container

    app.include_router(seller_router.router, prefix="/seller/v1")

    return TestClient(app)