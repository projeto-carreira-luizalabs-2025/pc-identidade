import os

import logging
from datetime import datetime

from fastapi import HTTPException, status

from app.api.common.auth_handler import UserAuthInfo
from app.clients.keycloak_admin_client import KeycloakAdminClient
from app.common.datetime import utcnow
from app.common.exceptions import BadRequestException, NotFoundException
from app.messages import (
    MSG_NOME_FANTASIA_JA_CADASTRADO,
    MSG_SELLER_CNPJ_NAO_ENCONTRADO,
    MSG_SELLER_ID_JA_CADASTRADO,
    MSG_SELLER_NAO_ENCONTRADO,
)
from app.models.seller_model import Seller
from app.models.seller_patch_model import SellerPatch
from app.repositories.seller_repository import SellerRepository
from app.api.v1.schemas.seller_schema import SellerCreate, SellerReplace
from ..models import Seller
from ..repositories import SellerRepository
from .base import CrudService

DEFAULT_USER = "system"

logger = logging.getLogger(__name__)


class SellerService(CrudService[Seller, str]):
    def __init__(self, repository: SellerRepository, keycloak_client: KeycloakAdminClient):
        super().__init__(repository)
        self.repository: SellerRepository = repository
        self.keycloak_client: KeycloakAdminClient = keycloak_client

    async def create(self, data: Seller, auth_info: UserAuthInfo) -> Seller:
        logger.info(f"Iniciando processo de criação para o seller_id: {data.seller_id}")
        # Verifica se seller_id já existe
        if await self.repository.find_by_id(data.seller_id):
            logger.warning(f"Tentativa de criar seller com ID duplicado: {data.seller_id}")
            raise BadRequestException(message=MSG_SELLER_ID_JA_CADASTRADO)

        # Verifica se trade_name já existe
        if await self.repository.find_by_trade_name(data.trade_name):
            logger.warning(f"Tentativa de criar seller com trade_name duplicado: {data.seller_id}")
            raise BadRequestException(message=MSG_NOME_FANTASIA_JA_CADASTRADO)

        user_identifier = f"{auth_info.user.server}:{auth_info.user.name}"

        now = utcnow()

        birth_date_as_datetime = datetime.combine(data.legal_rep_birth_date, datetime.min.time())

        seller_to_create = Seller(
            seller_id=data.seller_id,
            company_name=data.company_name,
            trade_name=data.trade_name,
            cnpj=data.cnpj,
            state_municipal_registration=data.state_municipal_registration,
            commercial_address=data.commercial_address,
            contact_phone=data.contact_phone,
            contact_email=data.contact_email,
            legal_rep_full_name=data.legal_rep_full_name,
            legal_rep_cpf=data.legal_rep_cpf,
            legal_rep_rg_number=data.legal_rep_rg_number,
            legal_rep_rg_state=data.legal_rep_rg_state,
            legal_rep_birth_date=birth_date_as_datetime,
            legal_rep_phone=data.legal_rep_phone,
            legal_rep_email=data.legal_rep_email,
            bank_name=data.bank_name,
            agency_account=data.agency_account,
            account_type=data.account_type,
            account_holder_name=data.account_holder_name,
            uploaded_documents=data.uploaded_documents,
            product_categories=data.product_categories,
            business_description=data.business_description,
            # Preenche os campos de auditoria
            created_at=now,
            updated_at=now,
            created_by=user_identifier,
            updated_by=user_identifier,
            audit_created_at=now,
            audit_updated_at=now,
        )

        logger.debug(f"Enviando dados do seller '{data.seller_id}' para o repositório.")
        created_seller = await self.repository.create(seller_to_create)
        logger.info(f"Seller '{data.seller_id}' criado com sucesso no banco de dados.")

        try:
            logger.debug(f"Atualizando usuário '{auth_info.user.name}' no Keycloak com o novo seller.")
            user_keycloak_id = auth_info.user.name  # O 'sub' do token

            # Pega os sellers atuais do usuário e adiciona o novo
            current_sellers = auth_info.sellers
            if data.seller_id not in current_sellers:
                updated_sellers = current_sellers + [data.seller_id]
                await self.keycloak_client.update_user_attributes(
                    user_id=user_keycloak_id,
                    attributes={"sellers": updated_sellers}
                )
                logger.info(f"Atributo 'sellers' do usuário '{auth_info.user.name}' atualizado no Keycloak.")

        except Exception as e:
            logger.error(
                f"Falha ao atualizar o usuário no Keycloak após criar o seller '{data.seller_id}'. Reversão manual pode ser necessária.",
                exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Seller criado, mas falha ao atualizar permissões do usuário.")

        return created_seller

    async def delete_by_id(self, entity_id) -> None:
        logger.info(f"Iniciando processo de exclusão para o seller_id: {entity_id}")
        deleted = await self.repository.delete_by_id(entity_id)
        if not deleted:
            logger.warning(f"Tentativa de excluir seller inexistente com ID: {entity_id}")
            raise NotFoundException(message=MSG_SELLER_NAO_ENCONTRADO.format(entity_id=entity_id))
        logger.info(f"Seller '{entity_id}' excluído com sucesso.")
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


    async def update(self, entity_id: str, data: SellerPatch, auth_info: UserAuthInfo) -> Seller:
        user_identifier = f"{auth_info.user.server}:{auth_info.user.name}"
        logger.info(f"Usuário '{user_identifier}' iniciando atualização (PATCH) para o seller_id: {entity_id}")
        current = await self.repository.find_by_id(entity_id)
        if not current:
            logger.warning(f"Usuário '{user_identifier}' tentou atualizar um seller inexistente: {entity_id}")
            raise NotFoundException(message=MSG_SELLER_NAO_ENCONTRADO.format(entity_id=entity_id))

        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            logger.info(f"Nenhum campo para atualizar no seller_id: {entity_id}. Nenhuma ação realizada.")
            return current

        if "trade_name" in update_data:
            existing = await self.repository.find_by_trade_name(update_data["trade_name"])
            if existing and existing.seller_id != entity_id:
                logger.warning(f"Tentativa de atualizar seller '{entity_id}' com trade_name que já está em uso.")
                raise BadRequestException(message=MSG_NOME_FANTASIA_JA_CADASTRADO)

        now = utcnow()

        update_data["updated_at"] = now
        update_data["updated_by"] = user_identifier
        update_data["audit_updated_at"] = now

        updated_seller = await self.repository.patch(entity_id, update_data)
        logger.info(f"Seller '{entity_id}' atualizado com sucesso pelo usuário '{user_identifier}'.")

        return updated_seller

    async def replace(self, entity_id: str, data: Seller, auth_info: UserAuthInfo) -> Seller:
        user_identifier = f"{auth_info.user.server}:{auth_info.user.name}"
        logger.info(f"Usuário '{user_identifier}' iniciando substituição (PUT) para o seller_id: {entity_id}")
        existing = await self.repository.find_by_id(entity_id)
        if not existing:
            logger.warning(f"Usuário '{user_identifier}' tentou substituir um seller inexistente: {entity_id}")
            raise NotFoundException(message=MSG_SELLER_NAO_ENCONTRADO.format(entity_id=entity_id))

        if await self.repository.find_by_trade_name(data.trade_name):
            if data.trade_name != existing.trade_name:
                logger.warning(
                    f"Conflito de nome fantasia ao tentar substituir o seller '{entity_id}'. "
                    f"O nome '{data.trade_name}' já está em uso."
                )
                raise BadRequestException(message=MSG_NOME_FANTASIA_JA_CADASTRADO)

        now = utcnow()

        logger.debug(f"Montando objeto de substituição para o seller '{entity_id}'.")
        updated_seller = Seller(
            seller_id=entity_id,
            company_name=data.company_name,
            trade_name=data.trade_name,
            cnpj=data.cnpj,
            state_municipal_registration=data.state_municipal_registration,
            commercial_address=data.commercial_address,
            contact_phone=data.contact_phone,
            contact_email=data.contact_email,
            legal_rep_full_name=data.legal_rep_full_name,
            legal_rep_cpf=data.legal_rep_cpf,
            legal_rep_rg_number=data.legal_rep_rg_number,
            legal_rep_rg_state=data.legal_rep_rg_state,
            legal_rep_birth_date=data.legal_rep_birth_date,
            legal_rep_phone=data.legal_rep_phone,
            legal_rep_email=data.legal_rep_email,
            bank_name=data.bank_name,
            agency_account=data.agency_account,
            account_type=data.account_type,
            account_holder_name=data.account_holder_name,
            uploaded_documents=data.uploaded_documents,
            product_categories=data.product_categories,
            business_description=data.business_description,
            created_at=existing.created_at,
            created_by=existing.created_by,
            updated_at=now,
            updated_by=user_identifier,
            audit_created_at=existing.audit_created_at,
            audit_updated_at=now,
        )

        result = await self.repository.update(entity_id, updated_seller)

        logger.info(f"Seller '{entity_id}' substituído com sucesso pelo usuário '{user_identifier}'.")

        return result
