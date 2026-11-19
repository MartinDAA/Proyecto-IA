from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.user import User
from app.repositories.implementations.in_memory_partida_repository import InMemoryPartidaRepository
from app.repositories.implementations.in_memory_user_repository import InMemoryUserRepository
from app.repositories.partida_repository import PartidaRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.partida_service import PartidaService
from ia_models.agentes import AgenteProgramado
from ia_models.escenarios import cargar_banco

# Instancias únicas: los repositorios en memoria deben compartirse entre peticiones.
_user_repository = InMemoryUserRepository()
_partida_repository = InMemoryPartidaRepository()


def get_user_repository() -> UserRepository:
    return _user_repository


def get_auth_service(users: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthService:
    return AuthService(users)


def get_partida_repository() -> PartidaRepository:
    return _partida_repository


def get_partida_service(
    partidas: Annotated[PartidaRepository, Depends(get_partida_repository)],
) -> PartidaService:
    return PartidaService(partidas, AgenteProgramado(), cargar_banco())


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    auth: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    user = auth.get_user_from_token(credentials.credentials) if credentials else None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
PartidaServiceDep = Annotated[PartidaService, Depends(get_partida_service)]
CurrentUser = Annotated[User, Depends(get_current_user)]
