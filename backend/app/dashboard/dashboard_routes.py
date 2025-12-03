from fastapi import APIRouter

from app.dashboard.dashboard_services import DashboardService

router = APIRouter()
dashboard_service = DashboardService()


@router.get("/bicicletas-estacionadas/{cnpj}")
async def bicicletas_estacionadas(cnpj: str):
    return await dashboard_service.bicicletas_estacionadas_por_ponto(cnpj)


@router.get("/problemas-por-avaliacao/{cnpj}")
async def problemas_por_avaliacao(cnpj: str):
    return await dashboard_service.problemas_por_avaliacao(cnpj)


@router.get("/taxa-ocupacao/{cnpj}")
async def taxa_ocupacao(cnpj: str):
    return await dashboard_service.taxa_ocupacao(cnpj)


@router.get("/receita-mensal/{cnpj}")
async def receita_mensal(cnpj: str):
    return await dashboard_service.receita_mensal(cnpj)


@router.get("/totens-ativos/{cnpj}")
async def totens_ativos(cnpj: str):
    return await dashboard_service.totens_ativos(cnpj)

