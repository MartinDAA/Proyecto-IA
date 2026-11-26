from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import partida_controller
from app.core.config import settings

app = FastAPI(title="K'iti Yachay API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(partida_controller.router)


@app.get("/api/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
