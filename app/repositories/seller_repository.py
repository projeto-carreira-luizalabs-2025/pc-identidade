from typing import Optional
from uuid import UUID

from app.common.exceptions import NotFoundException

from ..models import Seller
from .base import AsyncMemoryRepository


class SellerRepository(AsyncMemoryRepository[Seller, UUID]):

    def __init__(self):
        super().__init__(model_class=Seller)

    async def find_by_nome_fantasia(self, nome_fantasia: str) -> Optional[Seller]:
        """
        Busca um Seller pelo nome_fantasia.
        """
        result = next((s for s in self.memory if s.nome_fantasia == nome_fantasia), None)
        return result

    async def delete_by_id(self, seller_id: str) -> None:
        initial_len = len(self.memory)
        self.memory = [seller for seller in self.memory if seller.seller_id != seller_id]
        if len(self.memory) == initial_len:
            raise NotFoundException()


__all__ = ["SellerRepository"]
