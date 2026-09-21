from src.database.connection import get_db_context

class AdminModel:
    @staticmethod
    def reset_database():
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM itens_pedido")
            cursor.execute("DELETE FROM pedidos")
            cursor.execute("DELETE FROM produtos")
            cursor.execute("DELETE FROM usuarios")
            conn.commit()

    @staticmethod
    def executar_query(query: str):
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
