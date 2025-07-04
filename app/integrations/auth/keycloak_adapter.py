import httpx
import jwt
import logging
logger = logging.getLogger(__name__)

# ----- Exceções -----


class OAuthException(Exception):
    """Exceção geral de autenticação"""


class TokenExpiredException(OAuthException):
    """Token expirou"""


class InvalidTokenException(OAuthException):
    """Token inválido"""


class KeycloakAdapter:
    def __init__(self, well_known_url: str):
        with httpx.Client() as http_client:
            response = http_client.get(well_known_url)
            response.raise_for_status()
            well_known_data = response.json()
            jwks_uri = well_known_data["jwks_uri"]

        self.jwks_client = jwt.PyJWKClient(jwks_uri)

    async def validate_token(self, token: str) -> dict:
        try:
            logger.debug("Iniciando validação do token JWT.")
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)

            unverified_header = jwt.get_unverified_header(token)
            alg = unverified_header.get("alg")

            if not alg:
                raise InvalidTokenException("O token não especifica um algoritmo no cabeçalho.")

            info_token = jwt.decode(
                token,
                signing_key.key,
                algorithms=[alg],  # A correção está aqui
                options={"verify_aud": False},
            )
            logger.info(f"Token validado com sucesso para o usuário sub: {info_token.get('sub')}")
            return info_token
        except jwt.ExpiredSignatureError as exception:
            logger.warning("Tentativa de uso de token expirado.")
            raise TokenExpiredException("Token expirou") from exception
        except jwt.InvalidTokenError as exception:
            logger.warning(f"Token inválido recebido: {exception}")
            raise InvalidTokenException("Token inválido") from exception
        except Exception as e:
            logger.error("Erro inesperado durante a validação do token.", exc_info=True)
            raise OAuthException("Falha ao validar o token") from e
