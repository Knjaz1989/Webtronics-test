from a2wsgi import WSGIMiddleware
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles

from .admin.main import flask_app
from .auth.routes import user_router
from .site.routes import site_router
from .posts.routes import post_router


app = FastAPI()
api_router = APIRouter(prefix='/api', tags=['API'])

api_router.include_router(user_router)
api_router.include_router(post_router)

app.include_router(api_router)
app.include_router(site_router)

# Mount admin on flask
app.mount('/admin', WSGIMiddleware(flask_app))

# app.mount(
#     "/static",
#     StaticFiles(directory="static"),
#     name="static",
# )
