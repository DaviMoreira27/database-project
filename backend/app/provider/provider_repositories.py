import logging

import asyncpg
from app.database.database_service import DatabaseService
from app.provider.provider_error import ProviderQueryError
from app.provider.provider_types import ProviderTableResponse

logger = logging.getLogger(__name__)


class ProviderRepositories:
    def __init__(self):
        # Inicializa o serviço de banco de dados responsável pela conexão
        self._database_service = DatabaseService()

    @property
    def database_service(self):
        # Propriedade para acessar o serviço de banco de forma controlada
        return self._database_service

    async def get_provider_by_cnpj(self, cnpj: str):
        """
        Busca uma provedora pelo CNPJ.
        Retorna um objeto ProviderTableResponse ou None caso não exista.
        """
        try:
            # Obtém conexão com o banco (pool gerenciado pelo DatabaseService)
            conn = await self.database_service.db_connection()

            # Busca um único registro correspondente ao CNPJ informado
            row = await conn.fetchrow(
                "SELECT * FROM provedora WHERE cnpj = $1;",
                cnpj
            )

            # Caso nenhum registro seja encontrado, retornar None é apropriado
            if row is None:
                return None

            # Converte o registro retornado em um modelo Pydantic
            return ProviderTableResponse(**dict(row))

        except asyncpg.UndefinedColumnError as e:
            # Erro específico quando uma coluna usada na query não existe
            logger.error(f"Coluna inválida na tabela provedora: {e}")
            raise ProviderQueryError("Erro no schema da tabela provedora") from e

        except asyncpg.PostgresError as e:
            # Captura erros gerais do PostgreSQL
            logger.error(f"Erro SQL ao buscar provedora: {e}")
            raise ProviderQueryError("Falha ao consultar provedora") from e
