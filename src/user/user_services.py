from user_repositories import UserRepositories
from user_types import LoginBody
from fastapi import HTTPException
from database.database_error import InternalDatabaseError
import bcrypt
import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self._user_repositories = UserRepositories()

    async def login(self, data: LoginBody):
        try:
            email = data.email
            password = data.password.encode("utf-8")
            login_type = data.login_type

            user = await self._user_repositories.get_user(email, login_type)

            if user is None:
                raise HTTPException(status_code=401, detail="Email ou senha errados")

            if not bcrypt.checkpw(password, user.senha):
                raise HTTPException(status_code=401, detail="Email ou senha errados")

            return { "message": "Login efetuado com sucesso", "user": dict(user) }

        except InternalDatabaseError:
            raise HTTPException(
                status_code=500,
                detail="Erro interno, por favor tente novamente mais tarde"
            )

        except HTTPException:
            raise
