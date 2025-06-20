from typing import TYPE_CHECKING, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status

from app.api.common.schemas import ListResponse, Paginator, get_request_pagination
from app.container import Container
from app.models.seller_model import Seller
from app.models.seller_patch_model import SellerPatch

from ..schemas.seller_schema import SellerCreate, SellerReplace, SellerResponse, SellerUpdate
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
    summary="Listar todos os Sellers",
)
@inject
async def get(
    paginator: Paginator = Depends(get_request_pagination),
    cnpj: Optional[str] = Query(None),
    seller_service: "SellerService" = Depends(Provide[Container.seller_service]),
):
    """
    Retorna todos os sellers cadastrados no sistema
    """
    filters = {}
    if cnpj:
        filters["cnpj"] = cnpj
    results = await seller_service.find(paginator=paginator, filters=filters)
    return paginator.paginate(results=results)


@router.get(
    "/buscar",
    response_model=SellerResponse,
    name="Retorna Sellers por ID ou CNPJ",
    description="Buscar um Seller pelo seu 'seller_id' ou 'cnpj'",
    status_code=status.HTTP_200_OK,
    summary="Buscar Seller por ID ou CNPJ",
)
@inject
async def get_by_id_or_cnpj(
    seller_id: Optional[str] = Query(None, description="ID do Seller"),
    cnpj: Optional[str] = Query(None, description="CNPJ do Seller"),
    seller_service: "SellerService" = Depends(Provide[Container.seller_service]),
):
    """
    Retorna o seller correspondente ao seller_id ou cnpj.
    Pelo menos um dos parâmetros deve ser informado.
    """
    if not seller_id and not cnpj:
        raise ValueError("Informe seller_id ou cnpj para buscar o seller.")
    if seller_id and cnpj:
        raise ValueError("Informe apenas um dos parâmetros: seller_id ou cnpj.")
    if seller_id:
        return await seller_service.find_by_id(seller_id)
    else:
        return await seller_service.find_by_cnpj(cnpj)


@router.post(
    "",
    response_model=SellerResponse,
    name="Criar Seller",
    description="Cria um novo Seller",
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo Seller",
)
@inject
async def create(seller: SellerCreate, seller_service: "SellerService" = Depends(Provide[Container.seller_service]),):
    return await seller_service.create(seller)


@router.patch(
    "/{seller_id}",
    response_model=SellerResponse,
    name="Atualiza Seller",
    description="Atualizar um Seller pelo 'seller_id'",
    status_code=status.HTTP_200_OK,
    summary="Atualizar um Seller",
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
    # Converte apenas os campos que foram enviados na requisição
    patch_data = SellerPatch(**seller.dict(exclude_unset=True))
    return await seller_service.update(seller_id, patch_data)


@router.delete(
    "/{seller_id}",
    name="Remover Seller",
    description="Remove um Seller pelo 'seller_id'",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um Seller",
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


@router.put(
    "/{seller_id}",
    response_model=SellerResponse,
    name="Substitui Seller",
    description="Substitui completamente um Seller",
    status_code=status.HTTP_200_OK,
    summary="Atualizar Seller (completo)",
)
@inject
async def replace_by_id(
    seller_id: str,
    seller_data: SellerReplace,
    seller_service: "SellerService" = Depends(Provide[Container.seller_service]),
):
    seller = Seller(seller_id=seller_id, nome_fantasia=seller_data.nome_fantasia, cnpj=seller_data.cnpj)
    return await seller_service.replace(seller_id, seller)
