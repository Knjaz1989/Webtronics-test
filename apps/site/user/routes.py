from fastapi import APIRouter

from .schemas import TokenResponse
from .views import sign_up, login

user_router = APIRouter()


user_router.add_api_route("/sign_up", endpoint=sign_up, methods=['POST'])
user_router.add_api_route(
    "/login", endpoint=login, methods=['POST'],
    response_model=TokenResponse
)

