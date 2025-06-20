from app.common.datetime import utcnow
from app.common.exceptions.bad_request_exception import BadRequestException
from app.common.exceptions.not_found_exception import NotFoundException
from app.models.seller_model import Seller
from app.models.seller_patch_model import SellerPatch
from app.repositories.seller_repository import SellerRepository

from app.messages import (
    MSG_SELLER_ID_JA_CADASTRADO,
    MSG_NOME_FANTASIA_JA_CADASTRADO,
    MSG_SELLER_NAO_ENCONTRADO,
    MSG_SELLER_CNPJ_NAO_ENCONTRADO,
)

from ..models import Seller
from ..repositories import SellerRepository
from .base import CrudService

DEFAULT_USER = "system"

class SellerService(CrudService[Seller, str]):
    def __init__(self, repository: SellerRepository):
        super().__init__(repository)
        self.repository: SellerRepository = repository

    async def create(self, data: Seller) -> Seller:
        # Verifica se seller_id já existe
        if await self.repository.find_by_id(data.seller_id):
            raise BadRequestException(message=MSG_SELLER_ID_JA_CADASTRADO)

        # Verifica se nome_fantasia já existe
        if await self.repository.find_by_nome_fantasia(data.nome_fantasia):
            raise BadRequestException(message=MSG_NOME_FANTASIA_JA_CADASTRADO)

        return await self.repository.create(data)

    async def delete_by_id(self, entity_id) -> None:
        deleted = await self.repository.delete_by_id(entity_id)
        if not deleted:
            raise NotFoundException(message=MSG_SELLER_NAO_ENCONTRADO.format(entity_id=entity_id))
        return deleted

    async def find_by_id(self, seller_id: str) -> Seller:
        seller = await self.repository.find_by_id(seller_id)
        if not seller:
            raise NotFoundException(message=MSG_SELLER_NAO_ENCONTRADO.format(entity_id=seller_id))
        return seller
    
    async def find_by_cnpj(self, cnpj: str) -> Seller:
        seller = await self.repository.find_by_cnpj(cnpj)
        if not seller:
            raise NotFoundException(message=MSG_SELLER_CNPJ_NAO_ENCONTRADO.format(cnpj=cnpj))
        return seller

    async def update(self, entity_id: str, data: SellerPatch) -> Seller:
        current = await self.repository.find_by_id(entity_id)
        if not current:
            raise NotFoundException(message=MSG_SELLER_NAO_ENCONTRADO.format(entity_id=entity_id))

        update_data = {}
        if data.nome_fantasia is not None:
            existing = await self.repository.find_by_nome_fantasia(data.nome_fantasia)
            if existing and existing.seller_id != entity_id:
                raise BadRequestException(message=MSG_NOME_FANTASIA_JA_CADASTRADO)
            update_data["nome_fantasia"] = data.nome_fantasia
        if data.cnpj is not None:
            update_data["cnpj"] = data.cnpj

        if not update_data:
            return current 

        now = utcnow()
        update_data["updated_at"] = now
        update_data["updated_by"] = DEFAULT_USER
        update_data["audit_updated_at"] = now

        return await self.repository.patch(entity_id, update_data)

    async def replace(self, entity_id: str, data: Seller) -> Seller:
        existing = await self.repository.find_by_id(entity_id)
        if not existing:
            raise NotFoundException(message=MSG_SELLER_NAO_ENCONTRADO.format(entity_id=entity_id))

        if await self.repository.find_by_nome_fantasia(data.nome_fantasia):
            if data.nome_fantasia != existing.nome_fantasia:
                raise BadRequestException(message=MSG_NOME_FANTASIA_JA_CADASTRADO)

        now = utcnow()
        updated_seller = Seller(
            seller_id=entity_id,
            nome_fantasia=data.nome_fantasia,
            cnpj=data.cnpj,
            created_at=existing.created_at,
            updated_at=now,
            created_by=existing.created_by or DEFAULT_USER,
            updated_by=DEFAULT_USER,
            audit_created_at=existing.audit_created_at or now,
            audit_updated_at=now,
        )
        return await self.repository.update(entity_id, updated_seller)