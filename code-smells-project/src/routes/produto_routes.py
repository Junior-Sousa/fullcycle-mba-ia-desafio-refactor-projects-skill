from flask import Blueprint
from src.controllers.produto_controller import ProdutoController

produto_bp = Blueprint("produtos", __name__)

produto_bp.add_url_rule("/produtos", "listar_produtos", ProdutoController.listar, methods=["GET"])
produto_bp.add_url_rule("/produtos/busca", "buscar_produtos", ProdutoController.buscar_com_filtros, methods=["GET"])
produto_bp.add_url_rule("/produtos/<int:produto_id>", "buscar_produto", ProdutoController.buscar_por_id, methods=["GET"])
produto_bp.add_url_rule("/produtos", "criar_produto", ProdutoController.criar, methods=["POST"])
produto_bp.add_url_rule("/produtos/<int:produto_id>", "atualizar_produto", ProdutoController.atualizar, methods=["PUT"])
produto_bp.add_url_rule("/produtos/<int:produto_id>", "deletar_produto", ProdutoController.deletar, methods=["DELETE"])
