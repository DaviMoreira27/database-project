import logging

from fastapi import HTTPException

from app.dashboard.dashboard_error import DashboardQueryError
from app.dashboard.dashboard_repositories import (
    DashboardRepositories,
)
from app.database.database_error import InternalDatabaseError

logger = logging.getLogger(__name__)


class DashboardService:
    def __init__(self):
        self._repo = DashboardRepositories()

    async def bicicletas_estacionadas_por_ponto(self, cnpj: str):
        try:
            return await self._repo.bicicletas_estacionadas_por_ponto(cnpj)

        except (InternalDatabaseError, DashboardQueryError):
            logger.error("Erro ao consultar bicicletas estacionadas por ponto")
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao consultar bicicletas estacionadas"
            )

    async def problemas_por_avaliacao(self, cnpj: str):
        try:
            return await self._repo.problemas_por_avaliacao(cnpj)

        except (InternalDatabaseError, DashboardQueryError):
            logger.error("Erro ao consultar problemas por avaliação")
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao consultar problemas por avaliação"
            )

    async def taxa_ocupacao(self, cnpj: str):
        try:
            return await self._repo.taxa_ocupacao(cnpj)

        except (InternalDatabaseError, DashboardQueryError):
            logger.error("Erro ao consultar taxa de ocupação")
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao consultar taxa de ocupação"
            )

    async def receita_mensal(self, cnpj: str):
        try:
            return await self._repo.receita_mensal(cnpj)

        except (InternalDatabaseError, DashboardQueryError):
            logger.error("Erro ao consultar receita mensal")
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao consultar receita mensal"
            )

    async def sessoes_por_dia(self, cnpj: str):
        try:
            return await self._repo.sessoes_por_dia(cnpj)

        except (InternalDatabaseError, DashboardQueryError):
            logger.error("Erro ao consultar sessões por dia")
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao consultar sessões por dia"
            )
