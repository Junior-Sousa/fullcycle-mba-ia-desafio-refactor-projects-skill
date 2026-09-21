from werkzeug.security import generate_password_hash, check_password_hash
from src.database.connection import get_db_context

class UsuarioModel:
    @staticmethod
    def listar_todos():
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, email, tipo, criado_em FROM usuarios")
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def buscar_por_id(usuario_id: int):
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, email, tipo, criado_em FROM usuarios WHERE id = ?", (usuario_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def buscar_por_email_com_senha(email: str):
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, email, senha, tipo, criado_em FROM usuarios WHERE email = ?", (email,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def criar(nome: str, email: str, senha_plana: str, tipo: str = "cliente"):
        senha_hash = generate_password_hash(senha_plana)
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                (nome, email, senha_hash, tipo)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def autenticar(email: str, senha_plana: str):
        usuario = UsuarioModel.buscar_por_email_com_senha(email)
        if not usuario:
            return None

        # Suporte a senhas com hash e compatibilidade retroativa para senhas legadas em texto puro
        senha_armazenada = usuario["senha"]
        autenticado = False
        if senha_armazenada.startswith("pbkdf2:") or senha_armazenada.startswith("scrypt:"):
            autenticado = check_password_hash(senha_armazenada, senha_plana)
        else:
            autenticado = (senha_armazenada == senha_plana)

        if autenticado:
            # Retorna dados seguros sem o campo de senha
            return {
                "id": usuario["id"],
                "nome": usuario["nome"],
                "email": usuario["email"],
                "tipo": usuario["tipo"]
            }
        return None
