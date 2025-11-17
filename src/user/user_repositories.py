from database import database_service
from user_types import UserTableResponse

class UserRepositories:
    def __init__(self):
        self._database_service = database_service.DatabaseService()

    @property
    def database_service(self):
        return self._database_service

    async def get_user(self, email: str, type: str):
        dbConn = await self.database_service.db_connection();

        user = await dbConn.fetchrow(
            "SELECT * FROM Usuario WHERE email = $1 AND type = $2;",
            email,
            type,
            record_class=UserTableResponse
        )

        return user