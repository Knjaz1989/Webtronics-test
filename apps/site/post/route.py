from fastapi import APIRouter


post_router = APIRouter(
    prefix="/post",
    tags=["post"],
)
