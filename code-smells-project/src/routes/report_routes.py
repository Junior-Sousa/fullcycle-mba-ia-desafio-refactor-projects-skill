from flask import Blueprint
from src.controllers.report_controller import ReportController

report_bp = Blueprint("relatorios", __name__)

report_bp.add_url_rule("/relatorios/vendas", "relatorio_vendas", ReportController.relatorio_vendas, methods=["GET"])
