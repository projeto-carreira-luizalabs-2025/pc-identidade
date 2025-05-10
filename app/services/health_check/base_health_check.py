from app.settings import AppSettings

class BaseHealthCheck:
    def __init__(self, settings: AppSettings):
        self.settings = settings

    async def check_status(self):
        """Implementa a checagem do serviço. Deve lançar uma HealthCheckException se falhar"""
