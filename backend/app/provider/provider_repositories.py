import logging

import asyncpg
from app.database.database_service import DatabaseService
from app.provider.provider_error import ProviderQueryError
from app.provider.provider_types import ProviderTableResponse

logger = logging.getLogger(__name__)


class ProviderRepositories:
    def __init__(self):
        self._database_service = DatabaseService()

    @property
    def database_service(self):
        return self._database_service

    async def get_provider_by_cnpj(self, cnpj: str):
        try:
            conn = await self.database_service.db_connection()

            row = await conn.fetchrow(
                "SELECT * FROM provedora WHERE cnpj = $1;",
                cnpj
            )

            if row is None:
                return None

            return ProviderTableResponse(**dict(row))

        except asyncpg.UndefinedColumnError as e:
            logger.error(f"Coluna inválida na tabela provedora: {e}")
            raise ProviderQueryError("Erro no schema da tabela provedora") from e

        except asyncpg.PostgresError as e:
            logger.error(f"Erro SQL ao buscar provedora: {e}")
            raise ProviderQueryError("Falha ao consultar provedora") from e
