from fastapi import APIRouter

from user_types import LoginBody
from user_services import UserService


router = APIRouter()
user_service = UserService()

@router.post("/login")
async def login_user(body: LoginBody):
    return await user_service.login(body)
