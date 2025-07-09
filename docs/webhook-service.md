# Serviço de Webhook

Este documento descreve o serviço de webhook implementado para enviar mensagens de log quando sellers são alterados.

## Configuração

### Variáveis de Ambiente

Adicione a seguinte variável ao seu arquivo `.env`:

```properties
WEBHOOK_URL=https://hooks.slack.com/services/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
```

Esta URL será usada para enviar todas as mensagens de log.

## Funcionamento

### Mensagens Automáticas

O serviço envia automaticamente mensagens quando:

- **Seller Criado**: Quando um novo seller é criado
- **Seller Atualizado**: Quando um seller existente é atualizado (PATCH)
- **Seller Substituído**: Quando um seller existente é substituído (PUT)
- **Seller Excluído**: Quando um seller é marcado como inativo (soft delete)

### Formato das Mensagens

Todas as mensagens são enviadas no seguinte formato JSON:

```json
{
  "timestamp": "2025-07-06T10:30:00.000Z",
  "message": "Seller 'ABC123' foi atualizado",
  "changes": {
    "operation": "updated",
    "seller_id": "ABC123",
    "user": "keycloak:user123",
    "fields_changed": {
      "trade_name": "Novo Nome Fantasia",
      "contact_email": "novo@email.com"
    }
  }
}
```

### Exemplos de Mensagens

**Criação:**
```json
{
  "timestamp": "2025-07-06T10:30:00.000Z",
  "message": "Seller 'ABC123' foi criado",
  "changes": {
    "operation": "created",
    "seller_id": "ABC123",
    "user": "keycloak:user123"
  }
}
```

**Atualização:**
```json
{
  "timestamp": "2025-07-06T10:30:00.000Z",
  "message": "Seller 'ABC123' foi atualizado",
  "changes": {
    "operation": "updated",
    "seller_id": "ABC123",
    "user": "keycloak:user123",
    "fields_changed": {
      "trade_name": "Novo Nome",
      "contact_phone": "11999999999"
    }
  }
}
```

**Exclusão:**
```json
{
  "timestamp": "2025-07-06T10:30:00.000Z",
  "message": "Seller 'ABC123' foi marcado como inativo",
  "changes": {
    "operation": "deleted",
    "seller_id": "ABC123",
    "user": "keycloak:user123"
  }
}
```

## Tratamento de Erros

O serviço foi projetado para não interromper as operações principais em caso de falha no webhook:

- **Timeout**: Se o webhook não responder em 30 segundos, o erro será logado
- **Erro HTTP**: Erros de status HTTP são logados mas não impedem a operação
- **Erro de Rede**: Falhas de conectividade são tratadas e logadas
- **Erro Geral**: Qualquer outro erro é capturado e logado

## Logs

Todos os eventos relacionados ao webhook são logados:

- **Info**: Mensagens enviadas com sucesso
- **Error**: Falhas no envio de mensagens (não impedem a operação principal)

## Integração Automática

O webhook está integrado automaticamente com todas as operações de seller:

1. **Criação**: Após criar um seller e atualizar o Keycloak
2. **Atualização**: Após atualizar um seller (PATCH) - inclui quais campos foram alterados
3. **Substituição**: Após substituir um seller (PUT)
4. **Exclusão**: Após marcar um seller como inativo

## Exemplo de Fluxo

Quando você atualizar um seller através da API:

```http
PATCH /seller/v1/sellers/ABC123
Content-Type: application/json
Authorization: Bearer <seu-token>

{
  "trade_name": "Novo Nome Fantasia",
  "contact_email": "novo@email.com"
}
```

O sistema automaticamente:
1. Atualiza o seller no banco de dados
2. **Envia mensagem webhook** 📧 com as alterações específicas
3. Continua com o fluxo normal

## Configuração no Slack

O webhook enviará mensagens no formato JSON para o Slack. Para personalizar a apresentação, você pode configurar o webhook do Slack para processar os dados JSON conforme necessário.

## Segurança

- Todas as mensagens incluem informações do usuário que realizou a operação
- Timeout configurado para 30 segundos para evitar bloqueios
- Falhas no webhook não afetam as operações principais do sistema
