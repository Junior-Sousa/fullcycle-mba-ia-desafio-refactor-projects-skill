from src.models.health_model import HealthModel
from src.config.settings import Settings

class HealthService:
    @staticmethod
    def verificar_saude():
        counts = HealthModel.obter_contagem_tabelas()
        return {
            "status": "ok",
            "database": "connected",
            "counts": counts,
            "versao": "1.0.0",
            "ambiente": Settings.ENV,
            "db_path": Settings.DATABASE_PATH,
            "debug": Settings.DEBUG
        }
