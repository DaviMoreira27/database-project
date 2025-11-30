import logging

from app.dashboard.dashboard_types import (
    BicicletasEstacionadasResponse,
    ProblemasAvaliacoesResponse,
    ReceitaMensalResponse,
    SessoesPorDiaResponse,
    TaxaOcupacaoResponse,
)
from app.database.database_service import DatabaseService, InternalDatabaseError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DashboardRepositories:
    def __init__(self):
        self._database_service = DatabaseService()

    @property
    def db(self):
        return self._database_service

    async def bicicletas_estacionadas_por_ponto(self, cnpj: str):
        query = """
            SELECT
                pr.n_registro AS ponto_retirada,

                (
                    SELECT COUNT(*)
                    FROM bicicleta b2
                    WHERE b2.provedora = $1
                      AND b2.status = 'ESTACIONADO'
                ) AS total_estacionadas,

                (
                    SELECT COUNT(DISTINCT b.codigo)
                    FROM retirada_bicicleta rb
                    JOIN bicicleta b ON b.codigo = rb.bicicleta
                    WHERE rb.ponto_retirada = pr.n_registro
                      AND b.provedora = $1
                      AND b.status = 'ESTACIONADO'
                ) AS estacionadas_no_ponto,

                CASE
                    WHEN (
                        SELECT COUNT(*)
                        FROM bicicleta b2
                        WHERE b2.provedora = $1
                          AND b2.status = 'ESTACIONADO'
                    ) = 0 THEN 0
                    ELSE (
                        (
                            SELECT COUNT(DISTINCT b.codigo)
                            FROM retirada_bicicleta rb
                            JOIN bicicleta b ON b.codigo = rb.bicicleta
                            WHERE rb.ponto_retirada = pr.n_registro
                              AND b.provedora = $1
                              AND b.status = 'ESTACIONADO'
                        )::NUMERIC
                        /
                        (
                            SELECT COUNT(*)
                            FROM bicicleta b2
                            WHERE b2.provedora = $1
                              AND b2.status = 'ESTACIONADO'
                        )
                    )
                END AS percentual_relacional

            FROM pontos_de_retirada pr
            JOIN infraestrutura i ON i.n_registro = pr.n_registro
            WHERE i.provedora = $1
            ORDER BY percentual_relacional DESC;
        """

        try:
            conn = await self.db.db_connection()
            rows = await conn.fetch(query, cnpj)
            return [BicicletasEstacionadasResponse(**dict(r)) for r in rows]
        except Exception:
            logger.exception("Erro ao consultar bicicletas estacionadas por ponto")
            raise InternalDatabaseError

    async def problemas_por_avaliacao(self, cnpj: str):
        query = """
            SELECT
                i.n_registro,

                COALESCE(
                    (SELECT COUNT(*) FROM reporte_de_problema r WHERE r.infraestrutura = i.n_registro),
                    0
                ) AS problemas,

                COALESCE(
                    (SELECT COUNT(*) FROM avaliacao a WHERE a.infraestrutura = i.n_registro),
                    0
                ) AS avaliacoes,

                CASE
                    WHEN COALESCE(
                            (SELECT COUNT(*) FROM avaliacao a WHERE a.infraestrutura = i.n_registro),
                            0
                        ) = 0
                    THEN NULL
                    ELSE COALESCE(
                            (SELECT COUNT(*) FROM reporte_de_problema r WHERE r.infraestrutura = i.n_registro),
                            0
                        )::NUMERIC
                        /
                        (SELECT COUNT(*) FROM avaliacao a WHERE a.infraestrutura = i.n_registro)
                END AS razao_problema_por_avaliacao

            FROM infraestrutura i
            WHERE i.provedora = $1
            ORDER BY razao_problema_por_avaliacao DESC NULLS LAST;
        """

        try:
            conn = await self.db.db_connection()
            rows = await conn.fetch(query, cnpj)
            return [ProblemasAvaliacoesResponse(**dict(r)) for r in rows]
        except Exception:
            logger.exception("Erro ao consultar problemas por avaliação")
            raise InternalDatabaseError

    async def taxa_ocupacao(self, cnpj: str):
        query = """
            SELECT
                pr.n_registro,
                pr.capacidade,
                pr.bicicletas_disponiveis,
                (pr.bicicletas_disponiveis::NUMERIC / pr.capacidade) AS taxa_ocupacao
            FROM pontos_de_retirada pr
            JOIN infraestrutura i ON i.n_registro = pr.n_registro
            WHERE i.provedora = $1;
        """

        try:
            conn = await self.db.db_connection()
            rows = await conn.fetch(query, cnpj)
            return [TaxaOcupacaoResponse(**dict(r)) for r in rows]
        except Exception:
            logger.exception("Erro ao consultar taxa de ocupação")
            raise InternalDatabaseError

    async def receita_mensal(self, cnpj: str):
        query = """
            SELECT
                DATE_TRUNC('month', sr.data) AS mes,
                SUM(sr.valor) AS receita
            FROM sessao_recarga sr
            JOIN totens_de_recarga td ON td.n_registro = sr.totem
            JOIN infraestrutura i ON i.n_registro = td.n_registro
            WHERE i.provedora = $1
            GROUP BY DATE_TRUNC('month', sr.data)
            ORDER BY mes;
        """

        try:
            conn = await self.db.db_connection()
            rows = await conn.fetch(query, cnpj)
            return [ReceitaMensalResponse(**dict(r)) for r in rows]
        except Exception:
            logger.exception("Erro ao consultar receita mensal")
            raise InternalDatabaseError

    async def sessoes_por_dia(self, cnpj: str):
        query = """
            SELECT
                sr.data,
                COUNT(*) AS total_sessoes
            FROM sessao_recarga sr
            JOIN totens_de_recarga td ON td.n_registro = sr.totem
            JOIN infraestrutura i ON i.n_registro = td.n_registro
            WHERE i.provedora = $1
            GROUP BY sr.data
            ORDER BY sr.data;
        """

        try:
            conn = await self.db.db_connection()
            rows = await conn.fetch(query, cnpj)
            return [SessoesPorDiaResponse(**dict(r)) for r in rows]
        except Exception:
            logger.exception("Erro ao consultar sessões por dia")
            raise InternalDatabaseError
