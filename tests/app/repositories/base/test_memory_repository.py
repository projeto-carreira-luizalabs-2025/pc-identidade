
import pytest
from unittest import mock
from uuid import UUID

from app.repositories.base.memory_repository import AsyncMemoryRepository
from app.models.seller_model import Seller

@pytest.mark.asyncio
class TestAsyncMemoryRepository:
    async def test_create(self, mock_mongo_client):
        client, collection = mock_mongo_client
        model = Seller(
            seller_id="seller01",
            nome_fantasia="Loja Exemplo",
            cnpj="12345678000199"
        )
        collection.insert_one.return_value = mock.MagicMock()

        repo = AsyncMemoryRepository(client, "test_collection", Seller)
        result = await repo.create(model)

        collection.insert_one.assert_called_once()
        assert result.seller_id == model.seller_id

    async def test_find_by_id(self, mock_mongo_client):
        client, collection = mock_mongo_client
        collection.find_one.return_value = {
            "seller_id": "seller01",
            "nome_fantasia": "Loja Exemplo2 ",
            "cnpj": "12345678000199"
        }

        repo = AsyncMemoryRepository(client, "test_collection", Seller)
        result = await repo.find_by_id("seller01")

        assert result.seller_id == "seller01"

    async def test_find(self, mock_mongo_client):
        client, collection = mock_mongo_client
        doc = {
            "seller_id": "seller01",
            "nome_fantasia": "Loja Exemplo3",
            "cnpj": "12345678000199"
        }

        async def cursor_simulator():
            yield doc

        collection.find.return_value = mock.MagicMock()
        collection.find.return_value.skip.return_value = collection.find.return_value
        collection.find.return_value.limit.return_value = cursor_simulator()

        repo = AsyncMemoryRepository(client, "test_collection", Seller)
        result = await repo.find({"seller_id": "seller01"})

        assert len(result) == 1
        assert result[0].seller_id == "seller01"

    async def test_update(self, mock_mongo_client):
        client, collection = mock_mongo_client
        collection.find_one_and_update.return_value = {
            "seller_id": "seller01",
            "nome_fantasia": "Loja Atualizada",
            "cnpj": "12345678000199"
        }

        model = Seller(
            seller_id="seller01",
            nome_fantasia="Loja Atualizada",
            cnpj="12345678000199"
        )
        repo = AsyncMemoryRepository(client, "test_collection", Seller)
        result = await repo.update("seller01", model)

        assert result.nome_fantasia == "Loja Atualizada"

    async def test_delete_by_id(self, mock_mongo_client):
        client, collection = mock_mongo_client
        collection.delete_one.return_value = mock.MagicMock(deleted_count=1)

        repo = AsyncMemoryRepository(client, "test_collection", Seller)
        result = await repo.delete_by_id("seller01")

        assert result is True

    async def test_patch(self, mock_mongo_client):
        client, collection = mock_mongo_client
        collection.find_one_and_update.return_value = {
            "seller_id": "seller01",
            "nome_fantasia": "Loja Patch",
            "cnpj": "12345678000199"
        }

        repo = AsyncMemoryRepository(client, "test_collection", Seller)
        result = await repo.patch("seller01", {"nome_fantasia": "Loja Patch"})

        assert result.nome_fantasia == "Loja Patch"
