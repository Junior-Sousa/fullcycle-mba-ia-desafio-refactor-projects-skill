from flask import request, jsonify
from src.services.admin_service import AdminService

class AdminController:
    @staticmethod
    def reset_database():
        try:
            AdminService.reset_database()
            return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": f"Falha ao resetar banco: {str(e)}", "sucesso": False}), 500

    @staticmethod
    def executar_query():
        dados = request.get_json() or {}
        query = dados.get("sql", "").strip()

        resultado, erro, status_code = AdminService.executar_query(query)
        if erro:
            return jsonify({"erro": erro}), status_code

        return jsonify({"dados": resultado, "sucesso": True}), 200
