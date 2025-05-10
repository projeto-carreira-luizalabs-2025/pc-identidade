from fastapi import APIRouter, Depends
from app.services.health_check.service import HealthCheckService

routes = APIRouter()

@routes.get("/health")
def get_health(service: HealthCheckService = Depends()):
    return service.get_health()
