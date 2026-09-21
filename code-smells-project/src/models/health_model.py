from src.database.connection import get_db_context

class HealthModel:
    @staticmethod
    def obter_contagem_tabelas():
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM produtos")
            produtos = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            usuarios = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM pedidos")
            pedidos = cursor.fetchone()[0]

        return {
            "produtos": produtos,
            "usuarios": usuarios,
            "pedidos": pedidos
        }
