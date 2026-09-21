from flask import request, jsonify
from src.models.produto_model import ProdutoModel, CategoriaProduto

class ProdutoController:
    @staticmethod
    def listar():
        try:
            produtos = ProdutoModel.listar_todos()
            return jsonify({"dados": produtos, "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @staticmethod
    def buscar_por_id(produto_id: int):
        try:
            produto = ProdutoModel.buscar_por_id(produto_id)
            if produto:
                return jsonify({"dados": produto, "sucesso": True}), 200
            return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @staticmethod
    def buscar_com_filtros():
        try:
            termo = request.args.get("q", "")
            categoria = request.args.get("categoria", None)
            preco_min = request.args.get("preco_min", None)
            preco_max = request.args.get("preco_max", None)

            if preco_min is not None:
                preco_min = float(preco_min)
            if preco_max is not None:
                preco_max = float(preco_max)

            resultados = ProdutoModel.buscar_com_filtros(termo, categoria, preco_min, preco_max)
            return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @staticmethod
    def criar():
        try:
            dados = request.get_json()
            if not dados:
                return jsonify({"erro": "Dados inválidos"}), 400
            if "nome" not in dados:
                return jsonify({"erro": "Nome é obrigatório"}), 400
            if "preco" not in dados:
                return jsonify({"erro": "Preço é obrigatório"}), 400
            if "estoque" not in dados:
                return jsonify({"erro": "Estoque é obrigatório"}), 400

            nome = dados["nome"]
            descricao = dados.get("descricao", "")
            preco = dados["preco"]
            estoque = dados["estoque"]
            categoria = dados.get("categoria", CategoriaProduto.GERAL)

            if preco < 0:
                return jsonify({"erro": "Preço não pode ser negativo"}), 400
            if estoque < 0:
                return jsonify({"erro": "Estoque não pode ser negativo"}), 400
            if len(nome) < 2:
                return jsonify({"erro": "Nome muito curto"}), 400
            if len(nome) > 200:
                return jsonify({"erro": "Nome muito longo"}), 400

            if categoria not in CategoriaProduto.TODAS:
                return jsonify({"erro": f"Categoria inválida. Válidas: {CategoriaProduto.TODAS}"}), 400

            novo_id = ProdutoModel.criar(nome, descricao, preco, estoque, categoria)
            return jsonify({"dados": {"id": novo_id}, "sucesso": True, "mensagem": "Produto criado"}), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @staticmethod
    def atualizar(produto_id: int):
        try:
            dados = request.get_json()
            if not dados:
                return jsonify({"erro": "Dados inválidos"}), 400

            existente = ProdutoModel.buscar_por_id(produto_id)
            if not existente:
                return jsonify({"erro": "Produto não encontrado"}), 404

            if "nome" not in dados:
                return jsonify({"erro": "Nome é obrigatório"}), 400
            if "preco" not in dados:
                return jsonify({"erro": "Preço é obrigatório"}), 400
            if "estoque" not in dados:
                return jsonify({"erro": "Estoque é obrigatório"}), 400

            nome = dados["nome"]
            descricao = dados.get("descricao", "")
            preco = dados["preco"]
            estoque = dados["estoque"]
            categoria = dados.get("categoria", CategoriaProduto.GERAL)

            if preco < 0:
                return jsonify({"erro": "Preço não pode ser negativo"}), 400
            if estoque < 0:
                return jsonify({"erro": "Estoque não pode ser negativo"}), 400

            ProdutoModel.atualizar(produto_id, nome, descricao, preco, estoque, categoria)
            return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @staticmethod
    def deletar(produto_id: int):
        try:
            existente = ProdutoModel.buscar_por_id(produto_id)
            if not existente:
                return jsonify({"erro": "Produto não encontrado"}), 404

            ProdutoModel.deletar(produto_id)
            return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500
