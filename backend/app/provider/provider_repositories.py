import logging

import asyncpg
from app.database.database_service import DatabaseService, InternalDatabaseError
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

        except (asyncpg.exceptions.UndefinedColumnError, AttributeError):
            logger.fatal("Coluna errada ou faltante na tabela provedora.")
            raise InternalDatabaseError

        except Exception:
            logger.exception("Erro ao buscar provedora.")
            raise InternalDatabaseError
