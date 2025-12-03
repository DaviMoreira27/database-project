import logging

import asyncpg

from app.dashboard.dashboard_types import (
    BicicletasEstacionadasResponse,
    ProblemasAvaliacoesResponse,
    ReceitaMensalResponse,
    SessoesPorDiaResponse,
    TaxaOcupacaoResponse,
    TotensAtivosResponse,
)
from app.database.database_service import DatabaseService

logger = logging.getLogger(__name__)


class DashboardQueryError(Exception):
    pass


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

        except asyncpg.PostgresError as e:
            logger.error(f"Erro SQL em bicicletas_estacionadas_por_ponto: {e}")
            raise DashboardQueryError("Falha ao consultar bicicletas estacionadas") from e

    async def problemas_por_avaliacao(self, cnpj: str):
        query = """
            SELECT
                i.n_registro,
                COALESCE((SELECT COUNT(*) FROM reporte_de_problema r
                          WHERE r.infraestrutura = i.n_registro), 0) AS problemas,
                COALESCE((SELECT COUNT(*) FROM avaliacao a
                          WHERE a.infraestrutura = i.n_registro), 0) AS avaliacoes,
                CASE
                    WHEN COALESCE((SELECT COUNT(*) FROM avaliacao a
                                   WHERE a.infraestrutura = i.n_registro), 0) = 0
                    THEN NULL
                    ELSE COALESCE(
                            (SELECT COUNT(*) FROM reporte_de_problema r
                             WHERE r.infraestrutura = i.n_registro), 0
                        )::NUMERIC
                        /
                        (SELECT COUNT(*) FROM avaliacao a
                         WHERE a.infraestrutura = i.n_registro)
                END AS razao_problema_por_avaliacao
            FROM infraestrutura i
            WHERE i.provedora = $1
            ORDER BY razao_problema_por_avaliacao DESC NULLS LAST;
        """

        try:
            conn = await self.db.db_connection()
            rows = await conn.fetch(query, cnpj)
            return [ProblemasAvaliacoesResponse(**dict(r)) for r in rows]

        except asyncpg.PostgresError as e:
            logger.error(f"Erro SQL em problemas_por_avaliacao: {e}")
            raise DashboardQueryError("Falha ao consultar problemas por avaliação") from e

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

        except asyncpg.PostgresError as e:
            logger.error(f"Erro SQL em taxa_ocupacao: {e}")
            raise DashboardQueryError("Falha ao consultar taxa de ocupação") from e

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

        except asyncpg.PostgresError as e:
            logger.error(f"Erro SQL em receita_mensal: {e}")
            raise DashboardQueryError("Falha ao consultar receita mensal") from e

    async def totens_ativos(self, cnpj: str):
        query = """
            SELECT td.n_registro
            FROM totens_de_recarga td
            JOIN infraestrutura i ON i.n_registro = td.n_registro
            WHERE i.provedora = $1
            AND NOT EXISTS (
                SELECT 1
                FROM (
                    SELECT DISTINCT sr.data::date AS dia
                    FROM sessao_recarga sr
                    JOIN totens_de_recarga td2 ON td2.n_registro = sr.totem
                    JOIN infraestrutura i2 ON i2.n_registro = td2.n_registro
                    WHERE i2.provedora = $1
                ) dias_provedora
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM sessao_recarga sr2
                    WHERE sr2.totem = td.n_registro
                      AND sr2.data::date = dias_provedora.dia
                )
            );
        """

        try:
            conn = await self.db.db_connection()
            rows = await conn.fetch(query, cnpj)
            return [TotensAtivosResponse(**dict(r)) for r in rows]

        except asyncpg.PostgresError as e:
            logger.error(f"Erro SQL em totens_ativos: {e}")
            raise DashboardQueryError("Falha ao consultar totens ativos") from e

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

        except asyncpg.PostgresError as e:
            logger.error(f"Erro SQL em sessoes_por_dia: {e}")
            raise DashboardQueryError("Falha ao consultar sessões por dia") from e
