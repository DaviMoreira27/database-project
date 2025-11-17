from pydantic import BaseModel
from enum import Enum
from asyncpg import Record

from address import address_types

class LoginTypes(Enum):
    MANAGER = 1
    USER = 2
    ADMINISTRATOR = 3

class LoginBody(BaseModel):
    email: str
    password: str
    login_type: LoginTypes

class UserTableResponse(Record):
    cpf: str
    cargo: str
    endereco: address_types.AddressTableResponse
    nome: str
    email: str
    senha: str
    data_nascimento: str
