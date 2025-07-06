from typing import TYPE_CHECKING, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.common.auth_handler import do_auth, get_current_user_info, require_seller_permission, UserAuthInfo
from app.api.common.schemas import ListResponse, Paginator, get_request_pagination
from app.models.seller_model import Seller
from app.models.seller_patch_model import SellerPatch

from ..schemas.seller_schema import SellerCreate, SellerReplace, SellerResponse, SellerUpdate


if TYPE_CHECKING:
    from app.container import Container
    from app.services import SellerService


router = APIRouter(tags=["Sellers"])

# Constantes
SELLER_NOT_FOUND_OR_ACCESS_DENIED = "Seller não encontrado ou acesso não permitido"


async def _find_seller_by_id_with_access_check(seller_id: str, user_info: "UserAuthInfo", seller_service) -> "Seller":
    """Busca seller por ID com validação de acesso"""
    if seller_id not in user_info.sellers:
        raise HTTPException(status_code=404, detail=SELLER_NOT_FOUND_OR_ACCESS_DENIED)

    seller = await seller_service.find_by_id(seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller não encontrado")
    return seller


async def _find_seller_by_cnpj_with_access_check(cnpj: str, user_info: "UserAuthInfo", seller_service) -> "Seller":
    """Busca seller por CNPJ com validação de acesso"""
    seller = await seller_service.find_by_cnpj(cnpj)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller não encontrado")

    if seller.seller_id not in user_info.sellers:
        raise HTTPException(status_code=404, detail=SELLER_NOT_FOUND_OR_ACCESS_DENIED)

    return seller


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
    seller_service: "SellerService" = Depends(Provide["seller_service"]),
):
    """
    Retorna todos os sellers cadastrados no sistema
    """
    filters = {}
    results = await seller_service.find(
        filters=filters,
        limit=paginator.limit,
        offset=paginator.offset,
        sort=paginator.get_sort_order()
    )

    return paginator.paginate(results=results, filters=filters)


@router.get(
    "/buscar",
    response_model=SellerResponse,
    name="Buscar Seller por ID ou CNPJ",
    description="Buscar um Seller pelo 'seller_id' ou 'cnpj'. Se ambos forem fornecidos, deve bater os dois campos. Requer autorização.",
    status_code=status.HTTP_200_OK,
    summary="Buscar Seller por ID ou CNPJ",
)


@router.get(
    "/{seller_id}",
    response_model=SellerResponse,
    name="Buscar Seller por ID",
    description="Buscar um Seller pelo seu 'seller_id'. Requer autorização.",
    status_code=status.HTTP_200_OK,
    summary="Buscar Seller por ID",
    dependencies=[Depends(require_seller_permission)],
)
@inject
async def get_by_id(
    seller_id: str,
    seller_service: "SellerService" = Depends(Provide["seller_service"]),
):
    """
    Retorna os dados de um seller específico.
    O usuário autenticado precisa ter permissão para o seller_id informado.
    """
    return await seller_service.find_by_id(seller_id)


@router.post(
    "",
    response_model=SellerResponse,
    name="Criar Seller",
    description="Cria um novo Seller associado ao usuário autenticado.",
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo Seller",
)
@inject
async def create(
    seller: SellerCreate,
    seller_service: "SellerService" = Depends(Provide["seller_service"]),
    auth_info: UserAuthInfo = Depends(get_current_user_info),
):
    """
        Cria um novo seller. O seller será associado ao usuário autenticado.
    """
    seller_model = Seller(**seller.model_dump())
    return await seller_service.create(seller_model, auth_info)


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
    seller_service: "SellerService" = Depends(Provide["seller_service"]),
    auth_info: UserAuthInfo = Depends(require_seller_permission),
):
    """
    Atualiza os dados do seller. Pode alterar nome_fantasia e/ou cnpj.
    """
    patch_data = SellerPatch(**seller.model_dump(exclude_unset=True))
    return await seller_service.update(seller_id, patch_data, auth_info=auth_info)


@router.delete(
    "/{seller_id}",
    name="Remover Seller",
    description="Remove um Seller pelo 'seller_id'",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um Seller",
    dependencies=[Depends(require_seller_permission)],
)
@inject
async def delete_by_id(
    seller_id: str,
    seller_service: "SellerService" = Depends(Provide["seller_service"]),
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
    seller_service: "SellerService" = Depends(Provide["seller_service"]),
    auth_info: UserAuthInfo = Depends(require_seller_permission),
):
    seller = Seller(
        seller_id=seller_id,
        company_name=seller_data.company_name,
        trade_name=seller_data.trade_name,
        cnpj=seller_data.cnpj,
        state_municipal_registration=seller_data.state_municipal_registration,
        commercial_address=seller_data.commercial_address,
        contact_phone=seller_data.contact_phone,
        contact_email=seller_data.contact_email,
        legal_rep_full_name=seller_data.legal_rep_full_name,
        legal_rep_cpf=seller_data.legal_rep_cpf,
        legal_rep_rg_number=seller_data.legal_rep_rg_number,
        legal_rep_rg_state=seller_data.legal_rep_rg_state,
        legal_rep_birth_date=seller_data.legal_rep_birth_date,
        legal_rep_phone=seller_data.legal_rep_phone,
        legal_rep_email=seller_data.legal_rep_email,
        bank_name=seller_data.bank_name,
        agency_account=seller_data.agency_account,
        account_type=seller_data.account_type,
        account_holder_name=seller_data.account_holder_name,
        uploaded_documents=seller_data.uploaded_documents,
        product_categories=seller_data.product_categories,
        business_description=seller_data.business_description,
    )
    return await seller_service.replace(seller_id, seller, auth_info=auth_info)
