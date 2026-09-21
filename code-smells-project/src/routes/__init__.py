from .produto_routes import produto_bp
from .usuario_routes import usuario_bp
from .pedido_routes import pedido_bp
from .report_routes import report_bp
from .health_routes import health_bp
from .admin_routes import admin_bp

__all__ = [
    "produto_bp",
    "usuario_bp",
    "pedido_bp",
    "report_bp",
    "health_bp",
    "admin_bp"
]
