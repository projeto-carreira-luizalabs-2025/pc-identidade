from . import PersistableEntity


class Customer(PersistableEntity):
    name: str
    email: str
    tenant_id: str
