from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"erro": str(error.description if hasattr(error, "description") else error), "sucesso": False}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"erro": "Recurso não encontrado", "sucesso": False}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Erro interno não tratado: {str(error)}")
        return jsonify({"erro": "Erro interno do servidor", "sucesso": False}), 500
