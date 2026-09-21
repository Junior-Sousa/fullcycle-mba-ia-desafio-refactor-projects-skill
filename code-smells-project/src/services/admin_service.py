from src.models.admin_model import AdminModel

class AdminService:
    @staticmethod
    def reset_database():
        AdminModel.reset_database()

    @staticmethod
    def executar_query(query: str):
        query = (query or "").strip()
        if not query:
            return None, "Query não informada", 400

        # Bloqueio de empilhamento de comandos (query stacking)
        if ";" in query.rstrip(";"):
            return None, "Múltiplos comandos SQL não são permitidos", 400

        # Restrição de segurança: permitir estritamente leitura com SELECT
        normalized = query.upper()
        if not normalized.startswith("SELECT"):
            return None, "Execução restrita: Apenas consultas de leitura (SELECT) são permitidas por motivos de segurança. Para mutações, utilize os endpoints administrativos específicos.", 403

        # Blacklist de palavras-chave destrutivas ou perigosas
        forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "ATTACH", "PRAGMA", "EXEC"]
        tokens = [t.strip("(),;") for t in normalized.split()]
        if any(token in tokens for token in forbidden_keywords if token != "SELECT"):
            return None, "Comando proibido detectado na consulta", 403

        result = AdminModel.executar_query(query)
        return result, None, 200
