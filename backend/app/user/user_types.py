from datetime import date
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, model_validator


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


class ManagerTableResponse(BaseModel):
    cpf: str
    provedora: str


class UserWithProviderResponse(BaseModel):
    cpf: str
    cargo: str
    nome: str
    email: str
    senha: str
    data_nascimento: date
    provedora: str | None = None


class CreateUserBody(BaseModel):
    cpf: str = Field(..., max_length=11, min_length=11)
    cargo: str = Field(..., max_length=100)
    cep: str = Field(..., max_length=8, min_length=8)
    rua: str = Field(..., max_length=150)
    numero: str = Field(..., max_length=10)
    cidade: str = Field(..., max_length=150)
    uf: str = Field(..., max_length=2, min_length=2)
    nome: str = Field(..., max_length=150)
    email: EmailStr = Field(..., max_length=150)
    senha: str = Field(..., max_length=200)
    data_nascimento: date
    provedora: str | None = None  # obrigatório somente para gerente

    @model_validator(mode="after")
    def validar_provedora(self):
        if self.cargo.upper() == "GERENTE" and not self.provedora:
            raise ValueError("provedora é obrigatória para gerente")
        return self


class UserTypeFilter(BaseModel):
    cargo: LoginTypes
