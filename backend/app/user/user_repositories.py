import logging

import asyncpg

from app.database.database_service import DatabaseService, InternalDatabaseError
from app.user.user_types import (
    UserTableResponse,
    UserWithProviderResponse,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserRepositories:
    def __init__(self):
        self._database_service = DatabaseService()

    @property
    def database_service(self):
        return self._database_service

    async def get_user(self, email: str, cargo: str | None):
        try:
            dbConn = await self.database_service.db_connection()

            user = await dbConn.fetchrow(
                "SELECT * FROM usuario WHERE email = $1 AND cargo = $2;",
                email,
                cargo
            )

            if user is None:
                return None

            user_dict = dict(user)
            base_user = UserTableResponse(**user_dict)

            provedora = None

            if base_user.cargo == "GERENTE":
                gerente_data = await dbConn.fetchrow(
                    "SELECT * FROM gerente WHERE cpf = $1;",
                    base_user.cpf
                )

                if gerente_data:
                    provedora = gerente_data["provedora"]

            return UserWithProviderResponse(
                **dict(base_user),
                provedora=provedora
            )

        except (asyncpg.exceptions.UndefinedColumnError, AttributeError):
            logger.fatal("Coluna errada ou faltante na tabela")
            raise InternalDatabaseError


    async def list_users_by_type(self, cargo: str, cnpj: str | None):
        try:
            conn = await self.database_service.db_connection()
            if cnpj and cargo.upper() == "GERENTE":
                rows = await conn.fetch(
                    """
                    SELECT u.*
                    FROM usuario u
                    JOIN gerente g ON g.cpf = u.cpf
                    WHERE u.cargo = $1
                        AND g.provedora = $2;
                    """,
                    cargo,
                    cnpj
                )

            elif cnpj:
                rows = [] # Apenas o gerente ta associado por cnpj, se ele selecionou outro cargo nao tem pq voltar algo
            else:
                rows = await conn.fetch(
                    "SELECT * FROM usuario WHERE cargo = $1;",
                    cargo
                )

            result = []
            for r in rows:
                data = dict(r)
                data.pop("senha", None)
                result.append(data)

            return result

        except Exception:
            logger.exception("Erro ao listar usuários por tipo")
            raise InternalDatabaseError

    async def insert_user(self, data, provedora: str | None = None):
        try:
            conn = await self.database_service.db_connection()

            async with conn.transaction():

                # Inserir endereço (caso já exista, ignora)
                await conn.execute(
                    """
                        INSERT INTO endereco (cep, rua, numero, cidade, uf)
                        VALUES ($1, $2, $3, $4, $5)
                        ON CONFLICT (cep, rua, numero) DO NOTHING;
                    """,
                    data.cep,
                    data.rua,
                    data.numero,
                    data.cidade,
                    data.uf
                )

                # Inserção do usuário
                await conn.execute(
                    """
                        INSERT INTO usuario
                        (cpf, cargo, cep, rua, numero, nome, email, senha, data_nascimento)
                        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9);
                    """,
                    data.cpf,
                    data.cargo.upper(),
                    data.cep,
                    data.rua,
                    data.numero,
                    data.nome,
                    data.email,
                    data.senha,
                    data.data_nascimento
                )

                cargo_upper = data.cargo.upper()

                # Gerente
                if cargo_upper == "GERENTE":
                    if provedora is None:
                        raise InternalDatabaseError("Gerente precisa de uma provedora.")

                    await conn.execute(
                        """
                            INSERT INTO gerente (cpf, provedora)
                            VALUES ($1, $2);
                        """,
                        data.cpf,
                        provedora
                    )

                # Cliente
                elif cargo_upper == "CLIENTE":
                    await conn.execute(
                        """
                            INSERT INTO cliente (cpf, pontuacao)
                            VALUES ($1, 0);
                        """,
                        data.cpf
                    )

                # Administrador
                elif cargo_upper == "ADMINISTRADOR":
                    await conn.execute(
                        """
                            INSERT INTO administrador (cpf)
                            VALUES ($1);
                        """,
                        data.cpf
                    )

                else:
                    raise InternalDatabaseError("Cargo inválido.")

            return True

        except Exception:
            logger.exception("Erro ao inserir usuário.")
            raise InternalDatabaseError
