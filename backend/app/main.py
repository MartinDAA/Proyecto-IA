from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import auth_controller, partida_controller
from app.core.config import settings
from app.dependencies import get_user_repository
from app.services.auth_service import AuthService


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    auth = AuthService(get_user_repository())
    if auth.authenticate(settings.seed_admin_username, settings.seed_admin_password) is None:
        auth.register(settings.seed_admin_username, settings.seed_admin_password)
    yield


app = FastAPI(title="K'iti Yachay API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router)
app.include_router(partida_controller.router)


@app.get("/api/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
