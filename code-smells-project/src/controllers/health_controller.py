from flask import jsonify
from src.database.connection import get_db_context
from src.config.settings import Settings

class HealthController:
    @staticmethod
    def check():
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM produtos")
                produtos = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM usuarios")
                usuarios = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM pedidos")
                pedidos = cursor.fetchone()[0]

            return jsonify({
                "status": "ok",
                "database": "connected",
                "counts": {
                    "produtos": produtos,
                    "usuarios": usuarios,
                    "pedidos": pedidos
                },
                "versao": "1.0.0",
                "ambiente": Settings.ENV,
                "db_path": Settings.DATABASE_PATH,
                "debug": Settings.DEBUG
            }), 200
        except Exception as e:
            return jsonify({"status": "erro", "detalhes": str(e)}), 500
