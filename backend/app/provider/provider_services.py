import logging

from app.provider.provider_repositories import ProviderRepositories

logger = logging.getLogger(__name__)


class ProviderService:
    def __init__(self):
        self._provider_repositories = ProviderRepositories()

    async def find_provider(self, cnpj: str):
        provider = await self._provider_repositories.get_provider_by_cnpj(cnpj)
        return provider
