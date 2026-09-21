from src.database.connection import get_db_context
from src.models.pedido_model import StatusPedido

class ReportModel:
    @staticmethod
    def obter_dados_vendas_brutos():
        with get_db_context() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM pedidos")
            total_pedidos = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(total) FROM pedidos")
            faturamento = cursor.fetchone()[0] or 0.0

            cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", (StatusPedido.PENDENTE,))
            pendentes = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", (StatusPedido.APROVADO,))
            aprovados = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", (StatusPedido.CANCELADO,))
            cancelados = cursor.fetchone()[0] or 0

        return {
            "total_pedidos": total_pedidos,
            "faturamento": faturamento,
            "pendentes": pendentes,
            "aprovados": aprovados,
            "cancelados": cancelados
        }
