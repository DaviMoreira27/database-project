from pydantic import BaseModel


class AddressTableResponse(BaseModel):
    cep: str
    rua: str
    numero: str
    cidade: str
    uf: str
