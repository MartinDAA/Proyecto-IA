from app.core.security import create_access_token, decode_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    def register(self, username: str, password: str) -> User:
        return self._users.create(username, hash_password(password))

    def authenticate(self, username: str, password: str) -> User | None:
        user = self._users.get_by_username(username)
        if user is None or not verify_password(password, user.hashed_password):
            return None
        return user

    def login(self, username: str, password: str) -> str | None:
        """Devuelve un token de acceso, o None si las credenciales no son válidas."""
        user = self.authenticate(username, password)
        return create_access_token(user.username) if user else None

    def get_user_from_token(self, token: str) -> User | None:
        username = decode_access_token(token)
        return self._users.get_by_username(username) if username else None
