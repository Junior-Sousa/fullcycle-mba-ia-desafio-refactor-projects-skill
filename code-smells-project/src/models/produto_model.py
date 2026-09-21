from src.database.connection import get_db_context

class CategoriaProduto:
    INFORMATICA = "informatica"
    MOVEIS = "moveis"
    VESTUARIO = "vestuario"
    GERAL = "geral"
    ELETRONICOS = "eletronicos"
    LIVROS = "livros"

    TODAS = [INFORMATICA, MOVEIS, VESTUARIO, GERAL, ELETRONICOS, LIVROS]

class ProdutoModel:
    @staticmethod
    def listar_todos():
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, descricao, preco, estoque, categoria, ativo, criado_em FROM produtos")
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def buscar_por_id(produto_id: int):
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nome, descricao, preco, estoque, categoria, ativo, criado_em FROM produtos WHERE id = ?",
                (produto_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def buscar_com_filtros(termo: str = "", categoria: str = None, preco_min: float = None, preco_max: float = None):
        query = "SELECT id, nome, descricao, preco, estoque, categoria, ativo, criado_em FROM produtos WHERE 1=1"
        params = []

        if termo:
            query += " AND (nome LIKE ? OR descricao LIKE ?)"
            params.extend([f"%{termo}%", f"%{termo}%"])
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        if preco_min is not None:
            query += " AND preco >= ?"
            params.append(preco_min)
        if preco_max is not None:
            query += " AND preco <= ?"
            params.append(preco_max)

        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def criar(nome: str, descricao: str, preco: float, estoque: int, categoria: str):
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
                (nome, descricao, preco, estoque, categoria)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def atualizar(produto_id: int, nome: str, descricao: str, preco: float, estoque: int, categoria: str):
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE produtos SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ? WHERE id = ?",
                (nome, descricao, preco, estoque, categoria, produto_id)
            )
            conn.commit()
            return True

    @staticmethod
    def deletar(produto_id: int):
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            conn.commit()
            return True
