import logging

import bcrypt
from fastapi import HTTPException

from app.database.database_error import InternalDatabaseError
from app.provider.provider_services import ProviderService
from app.user.user_repositories import UserRepositories
from app.user.user_types import CreateUserBody, LoginBody, LoginTypes

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self):
        self._user_repositories = UserRepositories()
        self._provider_service = ProviderService()

    async def login(self, data: LoginBody):
        try:
            email = data.email
            password = data.password.encode("utf-8")
            login_type = data.login_type

            user = await self._user_repositories.get_user(email, login_type.value)

            if user is None:
                raise HTTPException(status_code=401, detail="Email ou senha errados")

            if not bcrypt.checkpw(password, user.senha.encode("utf-8")):
                raise HTTPException(status_code=401, detail="Email ou senha errados")

            return {
                "message": "Login efetuado com sucesso",
                "user": {k: v for (k, v) in dict(user).items() if k != "senha"},
                "error": None,
            }

        except InternalDatabaseError:
            raise HTTPException(
                status_code=500,
                detail="Erro interno, por favor tente novamente mais tarde",
            )

        except HTTPException:
            raise

    async def list_users(self, cargo: LoginTypes, cnpj: str | None):
        try:
            return await self._user_repositories.list_users_by_type(cargo.value, cnpj)
        except InternalDatabaseError:
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao listar usuários"
            )

    async def create_user(self, data: CreateUserBody):
        try:
            hashed = bcrypt.hashpw(
                data.senha.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            payload = data.model_copy()
            payload.senha = hashed
            cargo = payload.cargo.upper()

            check_user = await self._user_repositories.get_user(payload.email, payload.cargo)

            if (check_user is not None):
                raise HTTPException(
                    status_code=400,
                    detail="O email digitado ja existe na base de dados."
                )

            if cargo == "GERENTE" and payload.provedora is None:
                raise HTTPException(
                    status_code=400,
                    detail="Gerente precisa de uma provedora."
                )

            if payload.provedora:
                provedora = await self._provider_service.find_provider(payload.provedora)

                if (provedora is None):
                    raise HTTPException(
                        status_code=404,
                        detail="Provedora selecionada nao existe."
                    )

            await self._user_repositories.insert_user(
                payload,
                provedora=payload.provedora
            )

            return {
                "message": "Usuário criado com sucesso",
                "error": None
            }

        except InternalDatabaseError:
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao criar usuário."
            )
