from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.api.common.schemas import ListResponse, Paginator, UuidType, get_request_pagination
from app.container import Container

from ..schemas.seller_schema import SellerCreate, SellerResponse, SellerUpdate
from . import SELLER_PREFIX

if TYPE_CHECKING:
    from app.services import SellerService


router = APIRouter(prefix=SELLER_PREFIX, tags=["Sellers"])


@router.get(
    "",
    response_model=ListResponse[SellerResponse],
    name="Retorna todos os Sellers",
    description="Listar todos os Sellers",
    status_code=status.HTTP_200_OK,
    summary="Listar todos os Sellers"
)
@inject
async def get(
    paginator: Paginator = Depends(get_request_pagination),
    seller_service: "SellerService" = Depends(Provide[Container.seller_service]),
):
    """
    Retorna todos os sellers cadastrados no sistema
    """
    results = await seller_service.find(paginator=paginator, filters={})
    return paginator.paginate(results=results)


@router.get(
    "/{seller_id}",
    response_model=SellerResponse,
    name="Retorna Sellers por ID",
    description="Buscar um Seller pelo seu 'seller_id'",
    status_code=status.HTTP_200_OK,
    summary="Buscar Seller por ID"
)
@inject
async def get_by_id(
    seller_id: str,
    seller_service: "SellerService" = Depends(Provide[Container.seller_service]),
):
    """
    Retorna o seller correspondente ao seller_id"
    """
    return await seller_service.find_by_id(seller_id)


@router.post(
    "",
    response_model=SellerResponse,
    name="Criar Seller",
    description="Cria um novo Seller",
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo Seller"
)
@inject
async def create(
    seller: SellerCreate, seller_service: "SellerService" = Depends(Provide[Container.seller_service])
):
    """
    Cria um novo seller com ID único, nome fantasia exclusivo e CNPJ com 14 dígitos.
    """
    return await seller_service.create(seller)


@router.patch(
    "/{seller_id}",
    response_model=SellerResponse,
    name="Atualiza Seller",
    description="Atualizar um Seller pelo 'seller_id'",
    status_code=status.HTTP_200_OK,
    summary="Atualizar um Seller"
)
@inject
async def update_by_id(
    seller_id: str,
    seller: SellerUpdate,
    seller_service: "SellerService" = Depends(Provide[Container.seller_service]),
):
    """
    Atualiza os dados do seller. Pode alterar nome_fantasia e/ou cnpj.
    """
    return await seller_service.update(seller_id, seller)


@router.delete(
        "/{seller_id}", 
        name="Remover Seller",
        description="Remove um Seller pelo 'seller_id'",
        status_code=status.HTTP_204_NO_CONTENT, 
        summary="Remover um Seller"
)
@inject
async def delete_by_id(
    seller_id: str,
    seller_service: "SellerService" = Depends(Provide[Container.seller_service]),
):
    """
    Remove permanentemente o seller do sistema.
    """
    await seller_service.delete_by_id(seller_id)
