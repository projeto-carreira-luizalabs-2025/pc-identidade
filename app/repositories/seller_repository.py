from typing import Optional

from app.integrations.database.mongo_client import MongoClient

from ..models import Seller
from .base import AsyncMemoryRepository


class SellerRepository(AsyncMemoryRepository[Seller]):

    COLLECTION_NAME = "sellers"

    def __init__(self,client: "MongoClient"):
        super().__init__(client, collection_name=self.COLLECTION_NAME,model_class=Seller)

    async def find_by_nome_fantasia(self, nome_fantasia: str) -> Optional[Seller]:
        result = await self.collection.find_one({"nome_fantasia": nome_fantasia})
        if result:
            return self.model_class(**result)
        return None

    async def find_by_cnpj(self, cnpj: str) -> Optional[Seller]:
        result = await self.collection.find_one({"cnpj": cnpj})
        if result:
            return self.model_class(**result)
        return None

__all__ = ["SellerRepository"]
