from flask import jsonify
from src.services.report_service import ReportService

class ReportController:
    @staticmethod
    def summary_report():
        report = ReportService.get_summary_report()
        return jsonify(report), 200

    @staticmethod
    def user_report(user_id):
        report = ReportService.get_user_report(user_id)
        if not report:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        return jsonify(report), 200
