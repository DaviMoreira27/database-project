from fastapi import APIRouter

from app.user.user_services import UserService
from app.user.user_types import LoginBody

router = APIRouter()
user_service = UserService()


@router.post("/login")
async def login_user(body: LoginBody):
    return await user_service.login(body)
