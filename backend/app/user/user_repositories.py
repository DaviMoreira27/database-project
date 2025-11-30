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

    async def list_users_by_type(self, cargo: str):
        try:
            conn = await self.database_service.db_connection()
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
