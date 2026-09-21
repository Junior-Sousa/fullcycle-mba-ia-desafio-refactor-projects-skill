from flask import Blueprint
from src.controllers.health_controller import HealthController

health_bp = Blueprint("health", __name__)

health_bp.add_url_rule("/health", "health_check", HealthController.check, methods=["GET"])
