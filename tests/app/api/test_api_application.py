
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

from app.api.api_application import create_app

def test_create_app_structure(dummy_settings, dummy_router):
    app = create_app(dummy_settings, dummy_router)
    assert isinstance(app, FastAPI)
    assert app.title == dummy_settings.app_name
    assert app.version == dummy_settings.version
    assert app.openapi_url == dummy_settings.openapi_path
    assert app.openapi_version == "3.0.2"


def test_dummy_route_integration(dummy_settings, dummy_router):
    app = create_app(dummy_settings, dummy_router)
    client = TestClient(app)
    response = client.get("/dummy")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


def test_health_check_route(dummy_settings):
    router = APIRouter()
    app = create_app(dummy_settings, router)

    client = TestClient(app)
    response = client.get(f"{dummy_settings.health_check_base_path}/health")
    assert response.status_code == 200
    assert response.json() == {"version": "0.0.2"}