from asyncpg import Record

class AddressTableResponse(Record):
    cep: str
    rua: str
    numero: str
    cidade: str
    uf: str