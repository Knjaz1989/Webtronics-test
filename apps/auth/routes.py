from fastapi import APIRouter

from .schemas import TokenResponse
from .views import sign_up, login, delete_user

user_router = APIRouter(prefix="/user", tags=["user"])


user_router.add_api_route("/sign-up", endpoint=sign_up, methods=['POST'])
user_router.add_api_route(
    "/login", endpoint=login, methods=['POST'],
    response_model=TokenResponse
)
user_router.add_api_route(
    path='/', endpoint=delete_user, methods=['DELETE']
)
