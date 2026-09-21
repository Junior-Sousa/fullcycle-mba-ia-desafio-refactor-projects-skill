from src.models.usuario_model import UsuarioModel

class AuthService:
    @staticmethod
    def autenticar(email: str, senha: str):
        if not email or not senha:
            return None, "Email e senha são obrigatórios"

        usuario = UsuarioModel.autenticar(email, senha)
        if not usuario:
            return None, "Email ou senha inválidos"

        return usuario, None
