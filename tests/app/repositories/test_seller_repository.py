import pytest
from unittest import mock

from app.repositories.seller_repository import SellerRepository
from app.models.seller_model import Seller

nome_fantasia = "Loja Legal"
@pytest.mark.asyncio
class TestSellerRepository:
    async def test_find_by_nome_fantasia(self, mock_mongo_client):
        client, collection = mock_mongo_client
        collection.find_one = mock.AsyncMock(return_value={
            "seller_id": "seller01",
            "nome_fantasia": nome_fantasia,
            "cnpj": "12345678000199"
        })

        repo = SellerRepository(client)
        result = await repo.find_by_nome_fantasia(nome_fantasia)

        collection.find_one.assert_called_once_with({"nome_fantasia": nome_fantasia})
        assert isinstance(result, Seller)
        assert result.nome_fantasia == nome_fantasia

    async def test_find_by_nome_fantasia_not_found(self, mock_mongo_client):
        client, collection = mock_mongo_client
        collection.find_one = mock.AsyncMock(return_value=None)

        repo = SellerRepository(client)
        result = await repo.find_by_nome_fantasia("Loja Inexistente")

        assert result is None

    async def test_find_by_cnpj(self, mock_mongo_client):
        client, collection = mock_mongo_client
        collection.find_one = mock.AsyncMock(return_value={
            "seller_id": "seller02",
            "nome_fantasia": "Loja CNPJ",
            "cnpj": "99887766554433"
        })

        repo = SellerRepository(client)
        result = await repo.find_by_cnpj("99887766554433")

        collection.find_one.assert_called_once_with({"cnpj": "99887766554433"})
        assert isinstance(result, Seller)
        assert result.cnpj == "99887766554433"

    async def test_find_by_cnpj_not_found(self, mock_mongo_client):
        client, collection = mock_mongo_client
        collection.find_one = mock.AsyncMock(return_value=None)

        repo = SellerRepository(client)
        result = await repo.find_by_cnpj("00000000000000")

        assert result is None
