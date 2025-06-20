
from app.common.datetime import utcnow
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.seller_service import SellerService
from app.models.seller_model import Seller
from app.models.seller_patch_model import SellerPatch
from app.common.exceptions.bad_request_exception import BadRequestException
from app.common.exceptions.not_found_exception import NotFoundException

@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.find_by_id = AsyncMock()
    repo.find_by_nome_fantasia = AsyncMock()
    repo.find_by_cnpj = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete_by_id = AsyncMock()
    repo.patch = AsyncMock()
    return repo

@pytest.fixture
def seller_data():
    return Seller(
        seller_id="001",
        nome_fantasia="Loja X",
        cnpj="12345678901234",
        created_at=None,
        updated_at=None,
        created_by="test",
        updated_by="test",
        audit_created_at=None,
        audit_updated_at=None,
    )

@pytest.fixture
def patch_data():
    return SellerPatch(nome_fantasia="Nova Loja", cnpj="98765432109876")

@pytest.mark.asyncio
async def test_create_success(mock_repository, seller_data):
    mock_repository.find_by_id.return_value = None
    mock_repository.find_by_nome_fantasia.return_value = None
    mock_repository.create.return_value = seller_data

    service = SellerService(mock_repository)
    result = await service.create(seller_data)

    assert result == seller_data

@pytest.mark.asyncio
async def test_create_raises_if_id_exists(mock_repository, seller_data):
    mock_repository.find_by_id.return_value = seller_data

    service = SellerService(mock_repository)
    with pytest.raises(BadRequestException):
        await service.create(seller_data)

@pytest.mark.asyncio
async def test_create_raises_if_nome_fantasia_exists(mock_repository, seller_data):
    mock_repository.find_by_id.return_value = None
    mock_repository.find_by_nome_fantasia.return_value = seller_data

    service = SellerService(mock_repository)
    with pytest.raises(BadRequestException):
        await service.create(seller_data)

@pytest.mark.asyncio
async def test_update_patch_success(mock_repository, seller_data, patch_data):
    mock_repository.find_by_id.return_value = seller_data
    mock_repository.find_by_nome_fantasia.return_value = None
    mock_repository.patch.return_value = seller_data

    service = SellerService(mock_repository)
    result = await service.update("001", patch_data)

    assert result == seller_data

@pytest.mark.asyncio
async def test_update_patch_empty(mock_repository, seller_data):
    patch = SellerPatch()
    mock_repository.find_by_id.return_value = seller_data

    service = SellerService(mock_repository)
    result = await service.update("001", patch)

    # Verifica que patch não foi chamado
    mock_repository.patch.assert_not_called()

    # Verifica que o resultado é o mesmo objeto
    assert result is seller_data

@pytest.mark.asyncio
async def test_update_patch_nome_fantasia_exists(mock_repository, seller_data, patch_data):
    existing = Seller(**{**seller_data.dict(), "seller_id": "002"})
    mock_repository.find_by_id.return_value = seller_data
    mock_repository.find_by_nome_fantasia.return_value = existing

    service = SellerService(mock_repository)
    with pytest.raises(BadRequestException):
        await service.update("001", patch_data)

@pytest.mark.asyncio
async def test_update_patch_not_found(mock_repository, patch_data):
    mock_repository.find_by_id.return_value = None

    service = SellerService(mock_repository)
    with pytest.raises(NotFoundException):
        await service.update("001", patch_data)

@pytest.mark.asyncio
async def test_delete_success(mock_repository):
    mock_repository.delete_by_id.return_value = True

    service = SellerService(mock_repository)
    assert await service.delete_by_id("001") is True

@pytest.mark.asyncio
async def test_delete_not_found(mock_repository):
    mock_repository.delete_by_id.return_value = False

    service = SellerService(mock_repository)
    with pytest.raises(NotFoundException):
        await service.delete_by_id("001")

@pytest.mark.asyncio
async def test_find_by_id_success(mock_repository, seller_data):
    mock_repository.find_by_id.return_value = seller_data

    service = SellerService(mock_repository)
    result = await service.find_by_id("001")

    assert result == seller_data

@pytest.mark.asyncio
async def test_find_by_id_not_found(mock_repository):
    mock_repository.find_by_id.return_value = None

    service = SellerService(mock_repository)
    with pytest.raises(NotFoundException):
        await service.find_by_id("001")

@pytest.mark.asyncio
async def test_find_by_cnpj_success(mock_repository, seller_data):
    mock_repository.find_by_cnpj.return_value = seller_data

    service = SellerService(mock_repository)
    result = await service.find_by_cnpj("12345678901234")

    assert result == seller_data

@pytest.mark.asyncio
async def test_find_by_cnpj_not_found(mock_repository):
    mock_repository.find_by_cnpj.return_value = None

    service = SellerService(mock_repository)
    with pytest.raises(NotFoundException):
        await service.find_by_cnpj("12345678901234")

@pytest.mark.asyncio
async def test_replace_success(mock_repository, seller_data):
    mock_repository.find_by_id.return_value = seller_data
    mock_repository.find_by_nome_fantasia.return_value = None
    mock_repository.update.return_value = seller_data

    service = SellerService(mock_repository)
    result = await service.replace("001", seller_data)

    assert result == seller_data

@pytest.mark.asyncio
async def test_replace_conflict_nome_fantasia(mock_repository, seller_data):
    mock_repository.find_by_id.return_value = seller_data
    mock_repository.find_by_nome_fantasia.return_value = Seller(**{**seller_data.dict(), "nome_fantasia": "Outro", "seller_id": "002"})

    service = SellerService(mock_repository)
    with pytest.raises(BadRequestException):
        await service.replace("001", Seller(**{**seller_data.dict(), "nome_fantasia": "Outro"}))

@pytest.mark.asyncio
async def test_replace_not_found(mock_repository, seller_data):
    mock_repository.find_by_id.return_value = None

    service = SellerService(mock_repository)
    with pytest.raises(NotFoundException):
        await service.replace("001", seller_data)


@pytest.mark.asyncio
async def test_replace_with_same_existing_nome_fantasia(mock_repository, seller_data):
    # Simula que já existe um seller com o mesmo nome_fantasia
    mock_repository.find_by_id.return_value = seller_data
    mock_repository.find_by_nome_fantasia.return_value = seller_data  # mesmo objeto

    updated_seller = Seller(
        seller_id="001",
        nome_fantasia="Loja X",  # mesmo nome
        cnpj="12345678901234",
        created_by="tester",
        updated_by="tester",
        audit_created_at=utcnow(),
        audit_updated_at=utcnow(),
        created_at=utcnow(),
        updated_at=utcnow(),
    )

    service = SellerService(mock_repository)
    await service.replace("001", updated_seller)

    mock_repository.update.assert_called_once()
