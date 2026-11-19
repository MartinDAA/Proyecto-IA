from fastapi import APIRouter, HTTPException, status

from app.dependencies import AuthServiceDep, CurrentUser
from app.models.auth import LoginRequest, TokenResponse
from app.models.user import UserPublic

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
def login(credentials: LoginRequest, auth: AuthServiceDep) -> TokenResponse:
    token = auth.login(credentials.username, credentials.password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    return TokenResponse(access_token=token)


@router.get("/me")
def me(user: CurrentUser) -> UserPublic:
    return UserPublic(id=user.id, username=user.username)
