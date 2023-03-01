from fastapi.routing import APIRouter

from .views import get_main_page


site_router = APIRouter()

site_router.add_route(
    path='/', endpoint=get_main_page, methods=['GET']
)
