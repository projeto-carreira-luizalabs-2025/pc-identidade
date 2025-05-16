import re
from app.common.exceptions.application_exception import ApplicationException
from app.common.exceptions.bad_request_exception import BadRequestException
from app.common.exceptions.not_found_exception import NotFoundException
from app.models.seller_model import Seller
from app.repositories.seller_repository import SellerRepository
from ..models import Seller
from ..repositories import SellerRepository
from .base import CrudService


class SellerService(CrudService[Seller, str]):
    def __init__(self, repository: SellerRepository):
        super().__init__(repository)

    async def create(self, data: Seller) -> Seller:
        if not data.seller_id:
            raise BadRequestException(message="O seller_id é obrigatório.")
        if not re.fullmatch(r"^[a-z0-9]+$", data.seller_id):
            raise BadRequestException(message="O seller_id deve conter apenas letras minúsculas e números, sem espaços ou caracteres especiais.")

        try:
            await self.repository.find_by_id(data.seller_id)
            raise BadRequestException(message="O seller_id informado já está cadastrado. Escolha outro.")
        except NotFoundException:
            pass

        try:
            await self.repository.find_by_nome_fantasia(data.nome_fantasia)
            raise BadRequestException(message="O nome_fantasia informado já está cadastrado. Escolha outro.")
        except NotFoundException:
            pass
    
        if not data.cnpj or not data.cnpj.isdigit() or len(data.cnpj) != 14:
            raise BadRequestException(message="O CNPJ é inválido. Deve conter exatamente 14 dígitos numéricos.")


        return await self.repository.create(data)

    async def update(self, entity_id: str, data: Seller) -> Seller:
        try:
            existing = await self.repository.find_by_nome_fantasia(data.nome_fantasia)
            if existing.seller_id != entity_id:
                raise BadRequestException(message="O nome_fantasia informado já está cadastrado. Escolha outro.")
        except NotFoundException:
            pass

        if not data.cnpj or not data.cnpj.isdigit() or len(data.cnpj) != 14:
            raise BadRequestException(message="O CNPJ é inválido. Deve conter exatamente 14 dígitos numéricos.")

        
        return await self.repository.update(entity_id, data)
    
    async def delete_by_id(self, entity_id):
        await self.repository.find_by_id(entity_id)
        return await self.repository.delete_by_id(entity_id)
    
