from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel

from app.common.datetime import utcnow
from app.common.exceptions import NotFoundException

from .async_crud_repository import AsyncCrudRepository

T = TypeVar("T", bound=BaseModel)
ID = TypeVar("ID", bound=int | str)


class AsyncMemoryRepository(AsyncCrudRepository[T, ID], Generic[T, ID]):

    def __init__(self, model_class: type[T]):
        super().__init__()
        self.memory = []
        self.model_class = model_class

    async def create(self, entity: T) -> T:
        entity_dict = entity.model_dump(by_alias=True)
        entity_dict["created_at"] = utcnow()

        pydantic_entity = self.model_class(**entity_dict)
        self.memory.append(pydantic_entity)

        return pydantic_entity

    async def find_by_id(self, entity_id: ID) -> Optional[T]:
        # XXX Aqui eu sei que seller tem o id como o campo seller_id

        result = next((r for r in self.memory if getattr(r, "seller_id", None) == entity_id), None)
        if result:
            return result
    
        raise NotFoundException()

    async def find(self, filters: dict, limit: int = 10, offset: int = 0, sort: Optional[dict] = None) -> List[T]:

        filtered_list = [
            data
            for data in self.memory
            # TODO Criar filtro
        ]

        # XXX TODO Falta ordenar

        entities = []
        for document in filtered_list:
            entities.append(document)
        return entities

    async def update(self, entity_id: ID, entity: Any) -> T:
        # Converte a entidade para um dicionário, excluindo campos desnecessários
        entity_dict = entity.model_dump(by_alias=True, exclude={"identity"})
        entity_dict["updated_at"] = utcnow()

        # Busca o documento atual pelo ID
        current_document = await self.find_by_id(entity_id)

        if current_document:
            # Atualiza os dados do documento atual
            current_document_dict = current_document.model_dump(by_alias=True)
            current_document_dict.update(entity_dict)

            # Substitui o documento na memória
            self.memory = [
                current_document_dict if doc.seller_id == entity_id else doc
                for doc in self.memory
            ]

            # Retorna a entidade atualizada como uma instância do modelo
            return self.model_class(**current_document_dict)

        raise NotFoundException()

