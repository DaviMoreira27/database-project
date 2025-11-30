from datetime import date
from enum import Enum

from pydantic import BaseModel

from app.address.address_types import AddressTableResponse


class LoginTypes(Enum):
    MANAGER = "GERENTE"
    USER = "CLIENTE"
    ADMINISTRATOR = "ADMINISTRADOR"


class LoginBody(BaseModel):
    email: str
    password: str
    login_type: LoginTypes


class UserTableResponse(BaseModel):
    cpf: str
    cargo: str
    nome: str
    email: str
    senha: str
    data_nascimento: date


class CreateUserBody(BaseModel):
    cpf: str
    cargo: str
    cep: str
    rua: str
    numero: str
    cidade: str
    uf: str
    nome: str
    email: str
    senha: str
    data_nascimento: date
    provedora: str | None = None # obrigatório somente para gerente


class UserTypeFilter(BaseModel):
    cargo: LoginTypes
