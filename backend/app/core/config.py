from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Clave para firmar los JWT. Cámbiala con la variable de entorno SECRET_KEY fuera de desarrollo.
    secret_key: str = "dev-secret-key-cambiar-en-produccion-0123456789"
    access_token_expire_minutes: int = 60
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:4173"]

    # Usuario temporal para pruebas; se crea al arrancar la aplicación.
    seed_admin_username: str = "admin"
    seed_admin_password: str = "admin"


settings = Settings()
