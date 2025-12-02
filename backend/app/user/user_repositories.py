import logging

import asyncpg

from app.database.database_service import DatabaseService, InternalDatabaseError
from app.user.user_error import (
    UserInsertError,
    UserQueryError,
)
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
                "SELECT * FROM usuario WHERE email = $1 AND cargo = $2;", email, cargo
            )

            if user is None:
                return None

            user_dict = dict(user)
            base_user = UserTableResponse(**user_dict)

            provedora = None

            if base_user.cargo == "GERENTE":
                gerente_data = await dbConn.fetchrow(
                    "SELECT * FROM gerente WHERE cpf = $1;", base_user.cpf
                )

                if gerente_data:
                    provedora = gerente_data["provedora"]

            return UserWithProviderResponse(**dict(base_user), provedora=provedora)

        except asyncpg.UndefinedColumnError as e:
            logger.error(f"Coluna inválida na consulta get_user: {e}")
            raise UserQueryError("Erro no schema ao buscar usuário") from e

        except asyncpg.PostgresError as e:
            logger.error(f"Erro SQL em get_user: {e}")
            raise UserQueryError("Falha ao buscar usuário") from e
        except Exception as e:
            raise InternalDatabaseError(
                "Um erro inesperado ocorreu ao buscar o usuario"
            ) from e

    async def list_users_by_type(self, cargo: str, cnpj: str | None):
        try:
            cargo_upper = cargo.upper()

            if cargo_upper not in {"GERENTE", "CLIENTE", "ADMINISTRADOR"}:
                raise UserQueryError("Cargo inválido")

            conn = await self.database_service.db_connection()

            if cnpj and cargo_upper == "GERENTE":
                query = """
                    SELECT u.*
                    FROM usuario u
                    JOIN gerente g ON g.cpf = u.cpf
                    WHERE u.cargo = $1
                    AND g.provedora = $2;
                """
                rows = await conn.fetch(query, cargo_upper, cnpj)

            elif cnpj:
                # Não há associação de cnpj para outros cargos
                rows = []

            else:
                rows = await conn.fetch(
                    "SELECT * FROM usuario WHERE cargo = $1;", cargo_upper
                )

            result = []
            for r in rows:
                data = dict(r)
                data.pop("senha", None)
                result.append(data)

            return result

        except asyncpg.PostgresError as e:
            logger.error(f"Erro SQL ao listar usuários por tipo: {e}")
            raise UserQueryError("Falha ao consultar usuários") from e
        except Exception as e:
            raise InternalDatabaseError(
                "Um erro inesperado ocorreu ao listar usuarios"
            ) from e

    async def insert_user(self, data, provedora: str | None = None):
        try:
            conn = await self.database_service.db_connection()

            async with conn.transaction():
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
                    data.uf,
                )

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
                    data.data_nascimento,
                )

                cargo = data.cargo.upper()

                if cargo == "GERENTE":
                    if provedora is None:
                        raise UserInsertError("Gerente precisa de provedora")
                    await conn.execute(
                        "INSERT INTO gerente (cpf, provedora) VALUES ($1, $2);",
                        data.cpf,
                        provedora,
                    )

                elif cargo == "CLIENTE":
                    await conn.execute(
                        "INSERT INTO cliente (cpf, pontuacao) VALUES ($1, 0);", data.cpf
                    )

                elif cargo == "ADMINISTRADOR":
                    await conn.execute(
                        "INSERT INTO administrador (cpf) VALUES ($1);", data.cpf
                    )

                else:
                    raise UserInsertError("Cargo inválido")

            return True

        except asyncpg.UniqueViolationError as e:
            logger.warning(f"CPF, email ou endereco já cadastrado: {e}")
            raise UserInsertError(
                "O CPF, email ou endereco informado já estao associados a outro usuario"
            ) from e

        except asyncpg.DataError as e:
            if "value too long for type character varying" in str(e):
                raise UserInsertError("Algum campo excede o tamanho permitido") from e
            raise UserInsertError("Erro de dados inválidos no banco") from e

        except asyncpg.ForeignKeyViolationError as e:
            logger.error(f"Violação de FK em insert_user: {e}")
            raise UserInsertError("Dados relacionados não encontrados") from e

        except asyncpg.PostgresError as e:
            logger.error(f"Erro SQL inesperado em insert_user: {e}")
            raise UserInsertError("Erro ao inserir usuário") from e
        except Exception as e:
            raise InternalDatabaseError(
                "Um erro inesperado ocorreu ao inserir o usuario"
            ) from e
