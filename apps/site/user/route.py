from fastapi import APIRouter

from apps.site.user.view import get_main_page, get_login_page


user_router = APIRouter()


user_router.add_route("/", endpoint=get_main_page)
user_router.add_route("/login", endpoint=get_login_page)

