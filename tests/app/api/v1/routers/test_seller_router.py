from fastapi import status
from app.models.seller_model import Seller
from app.paths import SELLER_BASE, SELLER_GET_BY_ID

def test_get_sellers(client, mock_seller_service):
    mock_seller_service.find.return_value = [Seller(seller_id="1", nome_fantasia="Teste", cnpj="12345678000100")]

    response = client.get(SELLER_BASE)

    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.json()
    assert response.json()["results"][0]["seller_id"] == "1"


def test_get_by_id(client, mock_seller_service):
    mock_seller_service.find_by_id.return_value = Seller(seller_id="1", nome_fantasia="Teste", cnpj="12345678000100")

    response = client.get(f"{SELLER_GET_BY_ID}?seller_id=1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["seller_id"] == "1"


def test_get_by_cnpj(client, mock_seller_service):
    mock_seller_service.find_by_cnpj.return_value = Seller(seller_id="1", nome_fantasia="Teste", cnpj="12345678000100")

    response = client.get(f"{SELLER_GET_BY_ID}?cnpj=12345678000100")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["cnpj"] == "12345678000100"


def test_create_seller(client, mock_seller_service):
    seller_data = {"seller_id": "1", "nome_fantasia": "Teste", "cnpj": "12345678000100"}
    mock_seller_service.create.return_value = Seller(**seller_data)

    response = client.post(SELLER_BASE, json=seller_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["seller_id"] == "1"


def test_update_seller(client, mock_seller_service):
    updated = Seller(seller_id="1", nome_fantasia="Atualizado", cnpj="12345678000100")
    mock_seller_service.update.return_value = updated

    response = client.patch(f"{SELLER_BASE}/1", json={"nome_fantasia": "Atualizado"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome_fantasia"] == "Atualizado"


def test_replace_seller(client, mock_seller_service):
    replaced = Seller(seller_id="1", nome_fantasia="Novo", cnpj="12345678000100")
    mock_seller_service.replace.return_value = replaced

    response = client.put(f"{SELLER_BASE}/1", json={"nome_fantasia": "Novo", "cnpj": "12345678000100"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome_fantasia"] == "Novo"


def test_delete_seller(client, mock_seller_service):
    mock_seller_service.delete_by_id.return_value = None

    response = client.delete(f"{SELLER_BASE}/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT