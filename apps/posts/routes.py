from fastapi import APIRouter, status

from apps.posts import views as pv
from apps.posts.schemas import PostAddGetResponse, PostGetAllResponse


post_router = APIRouter(prefix="/post", tags=["post"])


post_router.add_api_route(
    path="/", endpoint=pv.get_current_post, methods=["GET"],
    response_model=PostAddGetResponse
)
post_router.add_api_route(
    path="/", endpoint=pv.add_post, methods=["POST"],
    response_model=PostAddGetResponse, status_code=status.HTTP_201_CREATED
)
post_router.add_api_route("/", endpoint=pv.delete_post, methods=["DELETE"])
post_router.add_api_route("/", endpoint=pv.change_post, methods=["PATCH"])

post_router.add_api_route(
    path="/all", endpoint=pv.get_all_posts, methods=["GET"],
    response_model=PostGetAllResponse
)
post_router.add_api_route("/search", endpoint=pv.search_post, methods=["GET"])

post_router.add_api_route("/rate", endpoint=pv.rate_post, methods=["POST"])
post_router.add_api_route("/rate", endpoint=pv.unrate_post, methods=["DELETE"])
