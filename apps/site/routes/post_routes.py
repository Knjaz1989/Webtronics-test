from fastapi import APIRouter

from apps.site.views.post_views import add_post, get_all_posts, delete_post, \
    change_post


post_router = APIRouter(prefix="/post", tags=["post"])

post_router.add_api_route("/add", endpoint=add_post, methods=["POST"])
post_router.add_api_route("/all", endpoint=get_all_posts, methods=["GET"])
post_router.add_api_route("/delete", endpoint=delete_post, methods=["POST"])
post_router.add_api_route("/update", endpoint=change_post, methods=["POST"])
