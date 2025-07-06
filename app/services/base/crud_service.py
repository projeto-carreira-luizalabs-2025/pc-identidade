from typing import Any, Generic, TypeVar, Optional, List

from app.api.common.schemas import Paginator
from app.common.exceptions.not_found_exception import NotFoundException
from app.models.base import PersistableEntity
from app.models.seller_model import Seller
from app.repositories import AsyncCrudRepository

T = TypeVar("T", bound=PersistableEntity)
ID = TypeVar("ID")


class CrudService(Generic[T, ID]):
    def __init__(self, repository: AsyncCrudRepository[T]):
        self.repository = repository

    @property
    def context(self):
        return None

    @property
    def author(self):
        # XXX Pegar depois
        return None

    async def create(self, entity: Any) -> T:
        return await self.repository.create(entity)

    async def find_by_id(self, entity_id: ID) -> T | None:
        return await self.repository.find_by_id(entity_id)

    async def find(self, filters: dict, limit: int, offset: int, sort: Optional[dict] = None) -> List[Seller]:
        """
        Busca sellers no repositório e repassa os parâmetros de paginação.
        """

        return await self.repository.find(
            filters=filters,
            limit=limit,
            offset=offset,
            sort=sort
        )

    async def update(self, entity_id: ID, entity: Any) -> T:
        return await self.repository.update(entity_id, entity)

    async def delete_by_id(self, entity_id: ID) -> None:
        await self.repository.delete_by_id(entity_id)
