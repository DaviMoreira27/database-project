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
