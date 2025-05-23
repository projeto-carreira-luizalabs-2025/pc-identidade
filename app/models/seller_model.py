from . import PersistableEntity


class Seller(PersistableEntity):
    seller_id: str
    nome_fantasia: str
    cnpj: str
