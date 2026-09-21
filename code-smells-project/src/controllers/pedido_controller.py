from flask import request, jsonify
from src.models.pedido_model import PedidoModel, StatusPedido

class PedidoController:
    @staticmethod
    def criar():
        try:
            dados = request.get_json()
            if not dados:
                return jsonify({"erro": "Dados inválidos"}), 400

            usuario_id = dados.get("usuario_id")
            itens = dados.get("itens", [])

            if not usuario_id:
                return jsonify({"erro": "Usuario ID é obrigatório"}), 400
            if not itens or len(itens) == 0:
                return jsonify({"erro": "Pedido deve ter pelo menos 1 item"}), 400

            resultado = PedidoModel.criar_pedido_transacional(usuario_id, itens)
            if "erro" in resultado:
                return jsonify({"erro": resultado["erro"], "sucesso": False}), 400

            return jsonify({
                "dados": resultado,
                "sucesso": True,
                "mensagem": "Pedido criado com sucesso"
            }), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @staticmethod
    def listar_todos():
        try:
            pedidos = PedidoModel.listar_todos()
            return jsonify({"dados": pedidos, "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @staticmethod
    def listar_por_usuario(usuario_id: int):
        try:
            pedidos = PedidoModel.listar_por_usuario(usuario_id)
            return jsonify({"dados": pedidos, "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @staticmethod
    def atualizar_status(pedido_id: int):
        try:
            dados = request.get_json() or {}
            novo_status = dados.get("status", "").strip().lower()

            if novo_status not in StatusPedido.TODOS:
                return jsonify({"erro": "Status inválido"}), 400

            PedidoModel.atualizar_status(pedido_id, novo_status)
            return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500
