from pydantic import BaseModel


class ProviderTableResponse(BaseModel):
    cnpj: str
