from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from apps.admin.main import flask_app
from apps.auth.routes import user_router
from apps.posts.routes import post_router


app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)


# Mount admin on flask
app.mount('/admin', WSGIMiddleware(flask_app))

# app.mount(
#     "/static",
#     StaticFiles(directory="apps/site/static/"),
#     name="static",
# )


# @app.on_event("startup")
# async def startup():
#     await engine.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await engine.disconnect()
