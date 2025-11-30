import logging

from app.provider.provider_error import ProviderQueryError
from app.provider.provider_repositories import ProviderRepositories
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class ProviderService:
    def __init__(self):
        self._provider_repositories = ProviderRepositories()

    async def find_provider(self, cnpj: str):
        try:
            provider = await self._provider_repositories.get_provider_by_cnpj(cnpj)
            return provider

        except ProviderQueryError as e:
            logger.error(f"Erro ao consultar provedora {cnpj}: {e}")
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao consultar provedora."
            )
