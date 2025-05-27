
import httpx
from fastapi import FastAPI


async def carregar_mock_sellers(app: FastAPI):

    # Aguarda alguns segundos para garantir que o servidor esteja escutando
    # await asyncio.sleep(1.5)

    mock_data = [
        {"seller_id": "mock1", "nome_fantasia": "loja do jose", "cnpj": "12345678901234"},
        {"seller_id": "mock2", "nome_fantasia": "mercado teste", "cnpj": "23456789012345"},
        {"seller_id": "mock3", "nome_fantasia": "vendas boas", "cnpj": "34567890123456"},
        {"seller_id": "mock4", "nome_fantasia": "mercado da gente", "cnpj": "24392107000190"}
    ]

    async with httpx.AsyncClient() as client:
        for seller in mock_data:
            try:
                response = await client.post("http://127.0.0.1:8000/seller/v1/sellers", json=seller)
                print(f"POST {seller['seller_id']} → {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Erro ao criar {seller['seller_id']}: {type(e).__name__} - {e}")
