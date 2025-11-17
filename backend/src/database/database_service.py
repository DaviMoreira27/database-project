import os
import asyncpg
import logging

logger = logging.getLogger(__name__)

class InternalDatabaseError(Exception):
    """Erro interno de conexão com o banco."""
    pass


class DatabaseService:
    def __init__(self):
        self._database_string = os.environ["DB_STRING"]

    @property
    def database_string(self):
        return self._database_string

    async def db_connection(self):
        try:
            return await asyncpg.connect(self.database_string)
        except (
            asyncpg.InvalidCatalogNameError,                 # banco não existe
            asyncpg.InvalidAuthorizationSpecificationError,  # user inválido
            asyncpg.InvalidPasswordError,                    # senha incorreta
            asyncpg.ConnectionDoesNotExistError,             # host/porta errados
            asyncpg.CannotConnectNowError,                   # servidor indisponível
            asyncpg.TooManyConnectionsError,                 # max connections
        ) as e:
            logger.error(f"Erro ao conectar no PostgreSQL: {e}")
            raise InternalDatabaseError("Falha interna ao conectar ao banco") from e

        except (OSError, ConnectionError) as e:
            logger.error(f"Erro de rede ao conectar no PostgreSQL: {e}")
            raise InternalDatabaseError("Falha interna ao conectar ao banco") from e

        except Exception as e:
            logger.error(f"Erro inesperado ao conectar no PostgreSQL: {e}")
            raise InternalDatabaseError("Falha interna ao conectar ao banco") from e
