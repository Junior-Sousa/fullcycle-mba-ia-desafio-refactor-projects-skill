"""Entry point da aplicação refatorada para o padrão MVC."""
import os
import sys

# Garante que o diretório raiz esteja no PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.app import app, create_app
from src.config.settings import Settings

if __name__ == "__main__":
    print("=" * 50)
    print("SERVIDOR INICIADO (MVC)")
    print(f"Rodando em http://{Settings.HOST}:{Settings.PORT}")
    print("=" * 50)
    app.run(host=Settings.HOST, port=Settings.PORT, debug=Settings.DEBUG)
