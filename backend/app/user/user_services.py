import logging

import bcrypt
from fastapi import HTTPException

from app.database.database_error import InternalDatabaseError
from app.provider.provider_services import ProviderService
from app.user.user_repositories import UserInsertError, UserQueryError, UserRepositories
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
            cargo = data.login_type.value

            user = await self._user_repositories.get_user(email, cargo)

            if user is None:
                raise HTTPException(status_code=401, detail="Email ou senha errados")

            if not bcrypt.checkpw(password, user.senha.encode("utf-8")):
                raise HTTPException(status_code=401, detail="Email ou senha errados")

            user_data = {k: v for (k, v) in dict(user).items() if k != "senha"}

            return {
                "message": "Login efetuado com sucesso",
                "user": user_data,
            }

        except InternalDatabaseError:
            logger.error("Erro de banco ao fazer login")
            raise HTTPException(
                status_code=500, detail="Erro interno. Tente novamente mais tarde."
            )

        except HTTPException:
            raise

    async def list_users(self, cargo: LoginTypes, cnpj: str | None):
        try:
            return await self._user_repositories.list_users_by_type(cargo.value, cnpj)

        except (InternalDatabaseError, UserQueryError):
            logger.error("Erro ao listar usuários")
            raise HTTPException(
                status_code=500, detail="Erro interno ao listar usuários."
            )

    async def create_user(self, data: CreateUserBody):
        try:
            hashed = bcrypt.hashpw(data.senha.encode("utf-8"), bcrypt.gensalt()).decode(
                "utf-8"
            )

            payload = data.model_copy()
            payload.senha = hashed

            cargo_upper = payload.cargo.upper()

            existing = await self._user_repositories.get_user(
                payload.email, payload.cargo
            )
            if existing is not None:
                raise HTTPException(
                    status_code=400,
                    detail="O email digitado já existe na base de dados.",
                )

            if cargo_upper == "GERENTE" and payload.provedora is None:
                raise HTTPException(
                    status_code=400, detail="Gerente precisa de uma provedora."
                )

            if payload.provedora:
                provedora = await self._provider_service.find_provider(
                    payload.provedora
                )
                if provedora is None:
                    raise HTTPException(
                        status_code=404, detail="Provedora selecionada não existe."
                    )

            await self._user_repositories.insert_user(payload, payload.provedora)

            return {"message": "Usuário criado com sucesso"}

        except InternalDatabaseError:
            logger.error("Erro ao inserir usuário")
            raise HTTPException(
                status_code=500, detail="Erro interno ao criar usuário."
            )
        except UserInsertError as e:
            raise HTTPException(status_code=400, detail=e.args[0])

        except HTTPException:
            raise
