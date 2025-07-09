import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import httpx
from app.services.webhook_service import WebhookService

ATUALIZADO = "📝 Atualizado"
NOVO_NOME_FANTASIA = "*Nome Fantasia:* Novo Nome" 
CAMPOS_ALTERADO = "*Campos alterados:*"
TESTE_MENSAGEM = "Test message"
NOVO_NOME = "Novo Nome"
URL_WEBHOOK = "https://hooks.slack.com/test"

class TestWebhookService:
    """Testes para o serviço de webhook"""
    
    @patch('app.services.webhook_service.settings')
    def test_init(self, mock_settings):
        """Testa inicialização do serviço"""
        mock_settings.WEBHOOK_URL = URL_WEBHOOK
        
        service = WebhookService()
        
        assert service.webhook_url == URL_WEBHOOK
        assert service.timeout == 30.0
    
    @patch('app.services.webhook_service.settings')
    @patch('app.services.webhook_service.httpx.AsyncClient')
    @patch('app.services.webhook_service.utcnow')
    async def test_send_update_message_success(self, mock_utcnow, mock_client, mock_settings):
        """Testa envio de mensagem com sucesso"""
        mock_settings.WEBHOOK_URL = URL_WEBHOOK
        mock_utcnow.return_value.timestamp.return_value = 1640995200
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
        
        service = WebhookService()
        
        message = "Seller atualizado"
        changes = {
            "operation": "updated",
            "seller_id": "001",
            "fields_changed": {"trade_name": NOVO_NOME}
        }
        
        result = await service.send_update_message(message, changes)
        
        assert result is True
        mock_client_instance.post.assert_called_once()
        
        # Verifica se o payload foi montado corretamente
        call_args = mock_client_instance.post.call_args
        assert call_args[0][0] == URL_WEBHOOK
        
        payload = call_args[1]['json']
        assert payload['text'] == "🔔 *Seller atualizado*"
        assert len(payload['attachments']) == 1
        assert payload['attachments'][0]['color'] == "warning"  # cor para "updated"
    
    @patch('app.services.webhook_service.settings')
    @patch('app.services.webhook_service.httpx.AsyncClient')
    @patch('app.services.webhook_service.utcnow')
    async def test_send_update_message_created_operation(self, mock_utcnow, mock_client, mock_settings):
        """Testa envio de mensagem para operação created"""
        mock_settings.WEBHOOK_URL = URL_WEBHOOK
        mock_utcnow.return_value.timestamp.return_value = 1640995200
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
        
        service = WebhookService()
        
        message = "Novo seller criado"
        changes = {
            "operation": "created",
            "seller_id": "001"
        }
        
        result = await service.send_update_message(message, changes)
        
        assert result is True
        
        # Verifica a cor para operação "created"
        payload = mock_client_instance.post.call_args[1]['json']
        assert payload['attachments'][0]['color'] == "good"
    
    @patch('app.services.webhook_service.settings')
    @patch('app.services.webhook_service.httpx.AsyncClient')
    @patch('app.services.webhook_service.utcnow')
    async def test_send_update_message_deleted_operation(self, mock_utcnow, mock_client, mock_settings):
        """Testa envio de mensagem para operação deleted"""
        mock_settings.WEBHOOK_URL = URL_WEBHOOK
        mock_utcnow.return_value.timestamp.return_value = 1640995200
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
        
        service = WebhookService()
        
        message = "Seller removido"
        changes = {
            "operation": "deleted",
            "seller_id": "001"
        }
        
        result = await service.send_update_message(message, changes)
        
        assert result is True
        
        # Verifica a cor para operação "deleted"
        payload = mock_client_instance.post.call_args[1]['json']
        assert payload['attachments'][0]['color'] == "danger"
    
    @patch('app.services.webhook_service.settings')
    @patch('app.services.webhook_service.httpx.AsyncClient')
    @patch('app.services.webhook_service.utcnow')
    async def test_send_update_message_replaced_operation(self, mock_utcnow, mock_client, mock_settings):
        """Testa envio de mensagem para operação replaced"""
        mock_settings.WEBHOOK_URL = URL_WEBHOOK
        mock_utcnow.return_value.timestamp.return_value = 1640995200
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
        
        service = WebhookService()
        
        message = "Seller substituído"
        changes = {
            "operation": "replaced",
            "seller_id": "001"
        }
        
        result = await service.send_update_message(message, changes)
        
        assert result is True
        
        # Verifica a cor para operação "replaced"
        payload = mock_client_instance.post.call_args[1]['json']
        assert payload['attachments'][0]['color'] == "#439FE0"
    
    @patch('app.services.webhook_service.settings')
    @patch('app.services.webhook_service.httpx.AsyncClient')
    async def test_send_update_message_timeout(self, mock_client, mock_settings):
        """Testa tratamento de timeout"""
        mock_settings.WEBHOOK_URL = URL_WEBHOOK
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = httpx.TimeoutException("Timeout")
        mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
        
        service = WebhookService()
        
        message = TESTE_MENSAGEM
        changes = {"operation": "updated"}
        
        result = await service.send_update_message(message, changes)
        
        assert result is False
    
    @patch('app.services.webhook_service.settings')
    @patch('app.services.webhook_service.httpx.AsyncClient')
    async def test_send_update_message_http_error(self, mock_client, mock_settings):
        """Testa tratamento de erro HTTP"""
        mock_settings.WEBHOOK_URL = URL_WEBHOOK
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=MagicMock(), response=mock_response
        )
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
        
        service = WebhookService()
        
        message = TESTE_MENSAGEM
        changes = {"operation": "updated"}
        
        result = await service.send_update_message(message, changes)
        
        assert result is False
    
    @patch('app.services.webhook_service.settings')
    @patch('app.services.webhook_service.httpx.AsyncClient')
    async def test_send_update_message_generic_exception(self, mock_client, mock_settings):
        """Testa tratamento de exceção genérica"""
        mock_settings.WEBHOOK_URL = URL_WEBHOOK
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = Exception("Generic error")
        mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
        
        service = WebhookService()
        
        message = TESTE_MENSAGEM
        changes = {"operation": "updated"}
        
        result = await service.send_update_message(message, changes)
        
        assert result is False
    
    def test_format_changes_with_operation(self):
        """Testa formatação de mudanças com operação"""
        service = WebhookService()
        
        changes = {
            "operation": "created",
            "seller_id": "001",
            "fields_changed": {"trade_name": NOVO_NOME, "cnpj": "12345678901234"}
        }
        
        result = service._format_changes(changes)
        
        assert "✨ Criado" in result
        assert CAMPOS_ALTERADO in result
        assert CAMPOS_ALTERADO in result
        assert NOVO_NOME_FANTASIA in result
        assert "*CNPJ:* 12345678901234" in result
    
    def test_format_changes_without_operation(self):
        """Testa formatação de mudanças sem operação"""
        service = WebhookService()
        
        changes = {
            "seller_id": "001",
            "fields_changed": {"trade_name": NOVO_NOME}
        }
        
        result = service._format_changes(changes)
        
        assert CAMPOS_ALTERADO in result
        assert CAMPOS_ALTERADO in result
        assert NOVO_NOME_FANTASIA in result
        assert "✨" not in result
        assert ATUALIZADO not in result 
    
    def test_format_changes_with_empty_fields_changed(self):
        """Testa formatação com fields_changed vazio"""
        service = WebhookService()
        
        changes = {
            "operation": "updated",
            "seller_id": "001",
            "fields_changed": {}
        }
        
        result = service._format_changes(changes)
        
        assert ATUALIZADO in result
        assert CAMPOS_ALTERADO not in result
    
    def test_format_changes_without_seller_id(self):
        """Testa formatação sem seller_id"""
        service = WebhookService()
        
        changes = {
            "operation": "updated",
            "fields_changed": {"trade_name": NOVO_NOME}
        }
        
        result = service._format_changes(changes)
        
        assert ATUALIZADO in result
        assert CAMPOS_ALTERADO in result
        assert NOVO_NOME_FANTASIA in result
        assert "*Seller ID:*" not in result
    
    def test_format_changes_minimal(self):
        """Testa formatação com dados mínimos"""
        service = WebhookService()
        
        changes = {}
        
        result = service._format_changes(changes)
        
        assert result.strip() == ""
