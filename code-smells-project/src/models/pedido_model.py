from src.database.connection import get_db_context

class StatusPedido:
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"

    TODOS = [PENDENTE, APROVADO, ENVIADO, ENTREGUE, CANCELADO]

class PedidoModel:
    @staticmethod
    def criar_pedido_transacional(usuario_id: int, itens: list):
        with get_db_context() as conn:
            cursor = conn.cursor()

            total = 0.0
            produtos_verificados = []

            for item in itens:
                produto_id = item["produto_id"]
                quantidade = item["quantidade"]

                cursor.execute("SELECT id, nome, preco, estoque FROM produtos WHERE id = ?", (produto_id,))
                prod = cursor.fetchone()
                if not prod:
                    return {"erro": f"Produto {produto_id} não encontrado"}
                if prod["estoque"] < quantidade:
                    return {"erro": f"Estoque insuficiente para {prod['nome']}"}

                subtotal = prod["preco"] * quantidade
                total += subtotal
                produtos_verificados.append({
                    "produto_id": prod["id"],
                    "quantidade": quantidade,
                    "preco_unitario": prod["preco"]
                })

            cursor.execute(
                "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, ?, ?)",
                (usuario_id, StatusPedido.PENDENTE, total)
            )
            pedido_id = cursor.lastrowid

            for item in produtos_verificados:
                cursor.execute(
                    "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                    (pedido_id, item["produto_id"], item["quantidade"], item["preco_unitario"])
                )
                cursor.execute(
                    "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                    (item["quantidade"], item["produto_id"])
                )

            conn.commit()
            return {"pedido_id": pedido_id, "total": total}

    @staticmethod
    def _agrupar_pedidos_com_itens(cursor):
        """Helper para carregar pedidos e itens sem N+1."""
        rows = cursor.fetchall()
        pedidos_dict = {}

        for row in rows:
            p_id = row["id"]
            if p_id not in pedidos_dict:
                pedidos_dict[p_id] = {
                    "id": p_id,
                    "usuario_id": row["usuario_id"],
                    "status": row["status"],
                    "total": row["total"],
                    "criado_em": row["criado_em"],
                    "itens": []
                }

            if row["item_id"]:
                pedidos_dict[p_id]["itens"].append({
                    "produto_id": row["produto_id"],
                    "produto_nome": row["produto_nome"] or "Desconhecido",
                    "quantidade": row["quantidade"],
                    "preco_unitario": row["preco_unitario"]
                })

        return list(pedidos_dict.values())

    @staticmethod
    def listar_todos():
        """Recupera todos os pedidos eliminando o gargalo N+1 através de consulta consolidada com LEFT JOIN."""
        query = """
            SELECT
                p.id, p.usuario_id, p.status, p.total, p.criado_em,
                ip.id AS item_id, ip.produto_id, ip.quantidade, ip.preco_unitario,
                pr.nome AS produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
            LEFT JOIN produtos pr ON ip.produto_id = pr.id
            ORDER BY p.id ASC
        """
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return PedidoModel._agrupar_pedidos_com_itens(cursor)

    @staticmethod
    def listar_por_usuario(usuario_id: int):
        """Recupera pedidos de um usuário específico em query única com LEFT JOIN."""
        query = """
            SELECT
                p.id, p.usuario_id, p.status, p.total, p.criado_em,
                ip.id AS item_id, ip.produto_id, ip.quantidade, ip.preco_unitario,
                pr.nome AS produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
            LEFT JOIN produtos pr ON ip.produto_id = pr.id
            WHERE p.usuario_id = ?
            ORDER BY p.id ASC
        """
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (usuario_id,))
            return PedidoModel._agrupar_pedidos_com_itens(cursor)

    @staticmethod
    def atualizar_status(pedido_id: int, novo_status: str):
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
            conn.commit()
            return True
