import logging

import asyncpg

from app.database.database_service import DatabaseService, InternalDatabaseError
from app.user.user_types import UserTableResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserRepositories:
    def __init__(self):
        self._database_service = DatabaseService()

    @property
    def database_service(self):
        return self._database_service

    async def get_user(self, email: str, type: str):
        try:
            dbConn = await self.database_service.db_connection()
            user = await dbConn.fetchrow(
                "SELECT * FROM Usuario WHERE email = $1 AND cargo = $2;", email, type
            )

            if user is None:
                return None

            logger.info("User: %s", {k: v for k, v in user.items() if k != "senha"})
            data = dict(user)
            record = UserTableResponse(**data)
            return record
        except (asyncpg.exceptions.UndefinedColumnError, AttributeError):
            logger.fatal("Coluna errada ou faltante na tabela")
            raise InternalDatabaseError
