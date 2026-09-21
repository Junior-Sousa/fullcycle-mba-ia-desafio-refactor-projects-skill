from flask import jsonify
from src.services.report_service import ReportService

class ReportController:
    @staticmethod
    def relatorio_vendas():
        try:
            relatorio = ReportService.gerar_relatorio_vendas()
            return jsonify({"dados": relatorio, "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500
