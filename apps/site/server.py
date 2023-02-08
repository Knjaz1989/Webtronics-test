from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apps.site.user.route import user_router


app = FastAPI()


app.include_router(user_router)


app.mount(
    "/static",
    StaticFiles(directory="apps/site/static/"),
    name="static",
)