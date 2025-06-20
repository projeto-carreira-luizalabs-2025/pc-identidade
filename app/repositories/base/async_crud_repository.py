from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
Q = TypeVar("Q")


class AsyncCrudRepository(ABC, Generic[T]):
    """
    Interface genérica para operações de repositório CRUD.
    """

    @abstractmethod
    async def create(self, entity: T) -> T:
        """
        Salva uma entidade no repositório.
        """

    @abstractmethod
    async def find_by_id(self,  seller_id: str) -> T | None:
        """
        Busca uma entidade pelo seu identificador único.
        """

    @abstractmethod
    async def find(self, filters: Q , limit: int = 20, offset: int = 0, sort: dict | None = None) -> list[T]:
        """
        Busca entidades no repositório, utilizando filtros e paginação.
        """

    @abstractmethod
    async def update(self, seller_id: str, entity: T) -> T:
        """
        Atualiza uma entidade existente no repositório.
        """

    @abstractmethod
    async def patch(self, seller_id: str, update_fields: dict) -> T | None:
        """
        Atualiza parcialmente uma entidade existente no repositório.
        """

    @abstractmethod
    async def delete_by_id(self, entity_id: str) -> bool:
        """
        Remove uma entidade pelo seu identificador único.
        """
