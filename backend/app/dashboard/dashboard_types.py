from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class BicicletasEstacionadasResponse(BaseModel):
    ponto_retirada: str
    total_estacionadas: int
    estacionadas_no_ponto: int
    percentual_relacional: float


class ProblemasAvaliacoesResponse(BaseModel):
    n_registro: str
    problemas: int
    avaliacoes: int
    razao_problema_por_avaliacao: Optional[float]


class TaxaOcupacaoResponse(BaseModel):
    n_registro: str
    capacidade: int
    bicicletas_disponiveis: int
    taxa_ocupacao: float


class ReceitaMensalResponse(BaseModel):
    mes: datetime
    receita: float


class TotensAtivosResponse(BaseModel):
    n_registro: str