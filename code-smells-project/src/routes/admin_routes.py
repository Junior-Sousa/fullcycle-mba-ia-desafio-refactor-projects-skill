from flask import Blueprint
from src.controllers.admin_controller import AdminController

admin_bp = Blueprint("admin", __name__)

admin_bp.add_url_rule("/admin/reset-db", "reset_database", AdminController.reset_database, methods=["POST"])
admin_bp.add_url_rule("/admin/query", "executar_query", AdminController.executar_query, methods=["POST"])
