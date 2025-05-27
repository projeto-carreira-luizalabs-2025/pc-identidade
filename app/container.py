from dependency_injector import containers, providers

from app.repositories import SellerRepository
from app.services import HealthCheckService, SellerService
from app.settings import AppSettings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(AppSettings)

    # Repositórios
    seller_repository = providers.Singleton(SellerRepository)

    # Serviços
    health_check_service = providers.Singleton(
        HealthCheckService, checkers=config.health_check_checkers, settings=settings
    )

    seller_service = providers.Singleton(SellerService, repository=seller_repository)
