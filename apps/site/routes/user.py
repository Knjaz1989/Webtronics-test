from fastapi import APIRouter

from apps.site.schemas.user import TokenResponse
from apps.site.views.user import sign_up, login

user_router = APIRouter(prefix="/user", tags=["user"])


user_router.add_api_route("/sign-up", endpoint=sign_up, methods=['POST'])
user_router.add_api_route(
    "/login", endpoint=login, methods=['POST'],
    response_model=TokenResponse
)
