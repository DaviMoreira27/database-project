from fastapi import APIRouter

from app.user.user_services import UserService
from app.user.user_types import CreateUserBody, LoginBody, LoginTypes

router = APIRouter()
user_service = UserService()


@router.post("/login")
async def login_user(body: LoginBody):
    return await user_service.login(body)

@router.get("/listar/{cargo}")
async def listar_usuarios(cargo: LoginTypes):
    return await user_service.list_users(cargo)


@router.post("/criar")
async def criar_usuario(body: CreateUserBody):
    return await user_service.create_user(body)
