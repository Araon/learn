from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.deps import db_session_middleware
from api.routes import permissions, roles, users
from cache.redis_client import redis
from core.database import engine, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await redis.aclose()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.middleware("http")(db_session_middleware)

app.include_router(users.router)
app.include_router(roles.router)
app.include_router(permissions.router)
