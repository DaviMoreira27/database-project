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
        # Repositório responsável por todas operações de banco
        self._user_repositories = UserRepositories()
        # Serviço que lida com provedores
        self._provider_service = ProviderService()

    async def login(self, data: LoginBody):
        try:
            email = data.email
            password = data.password.encode("utf-8")
            cargo = data.login_type.value  # Tipo de login determina o cargo

            # Busca usuário por email e cargo
            user = await self._user_repositories.get_user(email, cargo)

            # Se não existir, retorna erro genérico
            if user is None:
                raise HTTPException(status_code=401, detail="Email ou senha errados")

            # Verifica senha com bcrypt
            if not bcrypt.checkpw(password, user.senha.encode("utf-8")):
                raise HTTPException(status_code=401, detail="Email ou senha errados")

            # Remove senha da resposta
            user_data = {k: v for (k, v) in dict(user).items() if k != "senha"}

            return {
                "message": "Login efetuado com sucesso",
                "user": user_data,
            }

        except InternalDatabaseError:
            # Erros inesperados no banco
            logger.error("Erro de banco ao fazer login")
            raise HTTPException(
                status_code=500, detail="Erro interno. Tente novamente mais tarde."
            )

        except HTTPException:
            # Repassa erros já tratados
            raise

    async def list_users(self, cargo: LoginTypes, cnpj: str | None):
        try:
            # Apenas repassa para o repositório e lida com erros genéricos
            return await self._user_repositories.list_users_by_type(cargo.value, cnpj)

        except (InternalDatabaseError, UserQueryError):
            logger.error("Erro ao listar usuários")
            raise HTTPException(
                status_code=500, detail="Erro interno ao listar usuários."
            )

    async def create_user(self, data: CreateUserBody):
        try:
            # Gera hash da senha
            hashed = bcrypt.hashpw(data.senha.encode("utf-8"), bcrypt.gensalt()).decode(
                "utf-8"
            )

            # Copia payload e troca campo senha pelo hash
            payload = data.model_copy()
            payload.senha = hashed

            cargo_upper = payload.cargo.upper()

            # Verifica se email já existe
            existing = await self._user_repositories.get_user(
                payload.email, payload.cargo
            )
            if existing is not None:
                raise HTTPException(
                    status_code=400,
                    detail="O email digitado já existe na base de dados.",
                )

            # Gerente precisa de provedora
            if cargo_upper == "GERENTE" and payload.provedora is None:
                raise HTTPException(
                    status_code=400, detail="Gerente precisa de uma provedora."
                )

            # Valida se a provedora existe no sistema
            if payload.provedora:
                provedora = await self._provider_service.find_provider(
                    payload.provedora
                )
                if provedora is None:
                    raise HTTPException(
                        status_code=404, detail="Provedora selecionada não existe."
                    )

            # Insere no banco
            await self._user_repositories.insert_user(payload, payload.provedora)

            return {"message": "Usuário criado com sucesso"}

        except InternalDatabaseError:
            logger.error("Erro ao inserir usuário")
            raise HTTPException(
                status_code=500, detail="Erro interno ao criar usuário."
            )

        except UserInsertError as e:
            # Erro gerado pelo repositório → retorna como erro 400
            raise HTTPException(status_code=400, detail=e.args[0])

        except HTTPException:
            raise
