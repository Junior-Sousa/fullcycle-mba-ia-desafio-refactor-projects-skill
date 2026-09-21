from src.models.report_model import ReportModel

class ReportService:
    @staticmethod
    def gerar_relatorio_vendas():
        dados = ReportModel.obter_dados_vendas_brutos()
        total_pedidos = dados["total_pedidos"]
        faturamento = dados["faturamento"]

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
            "pedidos_pendentes": dados["pendentes"],
            "pedidos_aprovados": dados["aprovados"],
            "pedidos_cancelados": dados["cancelados"],
            "ticket_medio": ticket_medio
        }
