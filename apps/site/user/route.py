from fastapi import APIRouter

from apps.site.user import view

user_router = APIRouter()


user_router.add_api_route("/login", endpoint=view.login, methods=['POST'])
user_router.add_api_route("/sign_up", endpoint=view.sign_up, methods=['POST'])
