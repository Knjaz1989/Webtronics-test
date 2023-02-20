from fastapi import APIRouter

from apps.site.views import post_views as pv

post_router = APIRouter(prefix="/post", tags=["post"])

post_router.add_api_route("/create", endpoint=pv.add_post, methods=["POST"])
post_router.add_api_route("/all", endpoint=pv.get_all_posts, methods=["GET"])
post_router.add_api_route(
    "/current", endpoint=pv.get_current_post, methods=["GET"]
)
post_router.add_api_route("/delete", endpoint=pv.delete_post, methods=["POST"])
post_router.add_api_route("/update", endpoint=pv.change_post, methods=["POST"])
post_router.add_api_route("/rate", endpoint=pv.rate_post, methods=["POST"])
post_router.add_api_route("/unrate", endpoint=pv.unrate_post, methods=["POST"])
post_router.add_api_route("/search", endpoint=pv.search_post, methods=["GET"])
