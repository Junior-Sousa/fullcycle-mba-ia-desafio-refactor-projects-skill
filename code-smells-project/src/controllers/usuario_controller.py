from flask import request, jsonify
from src.models.usuario_model import UsuarioModel
from src.services.auth_service import AuthService

class UsuarioController:
    @staticmethod
    def listar():
        try:
            usuarios = UsuarioModel.listar_todos()
            return jsonify({"dados": usuarios, "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @staticmethod
    def buscar_por_id(usuario_id: int):
        try:
            usuario = UsuarioModel.buscar_por_id(usuario_id)
            if usuario:
                return jsonify({"dados": usuario, "sucesso": True}), 200
            return jsonify({"erro": "Usuário não encontrado"}), 404
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @staticmethod
    def criar():
        try:
            dados = request.get_json()
            if not dados:
                return jsonify({"erro": "Dados inválidos"}), 400

            nome = dados.get("nome", "").strip()
            email = dados.get("email", "").strip()
            senha = dados.get("senha", "")
            tipo = dados.get("tipo", "cliente")

            if not nome or not email or not senha:
                return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

            novo_id = UsuarioModel.criar(nome, email, senha, tipo)
            return jsonify({"dados": {"id": novo_id}, "sucesso": True}), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @staticmethod
    def login():
        try:
            dados = request.get_json() or {}
            email = dados.get("email", "").strip()
            senha = dados.get("senha", "")

            usuario, erro = AuthService.autenticar(email, senha)
            if erro:
                status_code = 400 if "obrigatórios" in erro else 401
                return jsonify({"erro": erro, "sucesso": False}), status_code

            return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500
