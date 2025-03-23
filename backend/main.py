from fastapi import FastAPI

from backend import routers

app = FastAPI()

app.include_router(routers.router)
