from flask import jsonify
from src.services.health_service import HealthService

class HealthController:
    @staticmethod
    def check():
        try:
            status_data = HealthService.verificar_saude()
            return jsonify(status_data), 200
        except Exception as e:
            return jsonify({"status": "erro", "detalhes": str(e)}), 500
