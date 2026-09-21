from src.database.connection import get_db_context
from src.models.pedido_model import StatusPedido

class ReportService:
    @staticmethod
    def gerar_relatorio_vendas():
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

            # Regras de desconto de negócio desacopladas
            desconto = 0.0
            if faturamento > 10000:
                desconto = faturamento * 0.10
            elif faturamento > 5000:
                desconto = faturamento * 0.05
            elif faturamento > 1000:
                desconto = faturamento * 0.02

            ticket_medio = round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0.0

            return {
                "total_pedidos": total_pedidos,
                "faturamento_bruto": round(faturamento, 2),
                "desconto_aplicavel": round(desconto, 2),
                "faturamento_liquido": round(faturamento - desconto, 2),
                "pedidos_pendentes": pendentes,
                "pedidos_aprovados": aprovados,
                "pedidos_cancelados": cancelados,
                "ticket_medio": ticket_medio
            }
