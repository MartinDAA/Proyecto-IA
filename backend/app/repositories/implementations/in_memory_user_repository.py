from threading import Lock

from app.models.user import User
from app.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    """Guarda los usuarios en memoria: se pierden al reiniciar. Solo para pruebas."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._next_id = 1
        self._lock = Lock()

    def get_by_username(self, username: str) -> User | None:
        return self._users.get(username)

    def create(self, username: str, hashed_password: str) -> User:
        with self._lock:
            if username in self._users:
                raise ValueError(f"El usuario '{username}' ya existe")
            user = User(id=self._next_id, username=username, hashed_password=hashed_password)
            self._users[username] = user
            self._next_id += 1
            return user
