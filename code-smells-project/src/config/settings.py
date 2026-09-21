import os

class Settings:
    """Configurações da aplicação centralizadas e desacopladas."""
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-padrao-desenvolvimento-segura-2026")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "loja.db")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    ENV = os.getenv("FLASK_ENV", "development")
