from flask import request, jsonify
from src.database.connection import get_db_context

class AdminController:
    @staticmethod
    def reset_database():
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM itens_pedido")
                cursor.execute("DELETE FROM pedidos")
                cursor.execute("DELETE FROM produtos")
                cursor.execute("DELETE FROM usuarios")
                conn.commit()
            return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": f"Falha ao resetar banco: {str(e)}", "sucesso": False}), 500

    @staticmethod
    def executar_query():
        dados = request.get_json() or {}
        query = dados.get("sql", "").strip()

        if not query:
            return jsonify({"erro": "Query não informada"}), 400

        # Bloqueio de empilhamento de comandos (query stacking)
        if ";" in query.rstrip(";"):
            return jsonify({"erro": "Múltiplos comandos SQL não são permitidos"}), 400

        # Restrição de segurança: permitir estritamente leitura com SELECT
        normalized = query.upper()
        if not normalized.startswith("SELECT"):
            return jsonify({
                "erro": "Execução restrita: Apenas consultas de leitura (SELECT) são permitidas por motivos de segurança. Para mutações, utilize os endpoints administrativos específicos."
            }), 403

        # Blacklist de palavras-chave destrutivas ou perigosas
        forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "ATTACH", "PRAGMA", "EXEC"]
        tokens = [t.strip("(),;") for t in normalized.split()]
        if any(token in tokens for token in forbidden_keywords if token != "SELECT"):
            return jsonify({"erro": "Comando proibido detectado na consulta"}), 403

        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
                return jsonify({"dados": result, "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 400
