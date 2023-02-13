from fastapi import APIRouter

from .views import add_post


post_router = APIRouter(
    prefix="/post",
    # tags=["post"],
)

post_router.add_api_route("/add", endpoint=add_post, methods=["POST"])
