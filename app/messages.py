# Descrições dos campos
DESC_SELLER_ID = "ID único, alfanumérico e lowercase"
DESC_NOME_FANTASIA = "Nome fantasia exclusivo no sistema"
DESC_CNPJ = "CNPJ com exatamente 14 dígitos numéricos, sem pontuação"

# Mensagens de erro
MSG_SELLER_ID_OBRIGATORIO = "O seller_id é obrigatório."
MSG_SELLER_ID_FORMATO = (
    "O seller_id deve conter apenas letras minúsculas e números, sem espaços ou caracteres especiais."
)
MSG_NOME_FANTASIA_CURTO = "O nome_fantasia deve conter ao menos 3 caracteres."
MSG_CNPJ_FORMATO = "O CNPJ deve conter exatamente 14 dígitos numéricos, sem pontuação."
MSG_CNPJ_FORMATO_REPLACE = "O CNPJ deve conter exatamente 14 dígitos numéricos."

# Descrições dos campos de erro
DESCRIPTION_ERROR = "Descrição do erro"
DESCRIPTION_LOCATION = "Descrição do erro"
DESCRIPTION_SLUG = "Identificação do erro"
DESCRIPTION_FIELD = "Campo que gerou o erro"
DESCRIPTION_CTX = "Contexto do erro"
DESCRIPTION_DETAILS = "Detalhes do erro"

MSG_SELLER_ID_JA_CADASTRADO = "O seller_id informado já está cadastrado. Escolha outro."
MSG_NOME_FANTASIA_JA_CADASTRADO = "O nome_fantasia informado já está cadastrado. Escolha outro."
MSG_SELLER_NAO_ENCONTRADO = "Seller com ID '{entity_id}' não encontrado."
MSG_SELLER_CNPJ_NAO_ENCONTRADO = "Nenhum Seller com CNPJ '{cnpj}' encontrado."

# Mensagens de sucesso
MSG_SELLER_CRIADO = "Seller criado com sucesso."
MSG_SELLER_ATUALIZADO = "Seller atualizado com sucesso."
MSG_SELLER_REMOVIDO = "Seller removido com sucesso."