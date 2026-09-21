from flask import Flask, jsonify
from flask_cors import CORS
from src.config.settings import Settings
from src.database.connection import init_db
from src.middlewares.error_handler import register_error_handlers
from src.routes import (
    produto_bp,
    usuario_bp,
    pedido_bp,
    report_bp,
    health_bp,
    admin_bp
)

def create_app():
    """Application Factory para instanciacao da aplicacao Flask desacoplada."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Settings.SECRET_KEY
    app.config["DEBUG"] = Settings.DEBUG

    CORS(app)

    # Inicializa banco de dados e sementes
    init_db(Settings.DATABASE_PATH)

    # Registra tratamento centralizado de erros
    register_error_handlers(app)

    # Registra Blueprints organizados por dominio
    app.register_blueprint(produto_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def index():
        return jsonify({
            "mensagem": "Bem-vindo à API da Loja",
            "versao": "1.0.0",
            "endpoints": {
                "produtos": "/produtos",
                "usuarios": "/usuarios",
                "pedidos": "/pedidos",
                "login": "/login",
                "relatorios": "/relatorios/vendas",
                "health": "/health"
            }
        })

    return app

app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("SERVIDOR INICIADO (MVC)")
    print(f"Rodando em http://{Settings.HOST}:{Settings.PORT}")
    print("=" * 50)
    app.run(host=Settings.HOST, port=Settings.PORT, debug=Settings.DEBUG)
