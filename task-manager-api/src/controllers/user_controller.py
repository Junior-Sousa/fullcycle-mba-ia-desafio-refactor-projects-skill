from flask import request, jsonify
from src.database.connection import db
from src.models.user_model import User
from src.models.task_model import Task
import re

class UserController:
    @staticmethod
    def get_users():
        users = User.query.all()
        result = []
        for u in users:
            user_data = u.to_dict()
            user_data['task_count'] = len(u.tasks)
            result.append(user_data)
        return jsonify(result), 200

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        data = user.to_dict()
        data['tasks'] = [t.to_dict() for t in user.tasks]
        return jsonify(data), 200

    @staticmethod
    def create_user():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        if not name:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        if not email:
            return jsonify({'error': 'Email é obrigatório'}), 400
        if not password:
            return jsonify({'error': 'Senha é obrigatória'}), 400

        if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
            return jsonify({'error': 'Email inválido'}), 400

        if len(password) < 4:
            return jsonify({'error': 'Senha deve ter no mínimo 4 caracteres'}), 400

        existing = User.query.filter_by(email=email).first()
        if existing:
            return jsonify({'error': 'Email já cadastrado'}), 409

        if role not in ['user', 'admin', 'manager']:
            return jsonify({'error': 'Role inválido'}), 400

        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        user.role = role

        try:
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Erro ao criar usuário'}), 500

    @staticmethod
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400

        if 'name' in data:
            user.name = data['name']

        if 'email' in data:
            if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', data['email']):
                return jsonify({'error': 'Email inválido'}), 400

            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'Email já cadastrado'}), 409
            user.email = data['email']

        if 'password' in data:
            if len(data['password']) < 4:
                return jsonify({'error': 'Senha muito curta'}), 400
            user.set_password(data['password'])

        if 'role' in data:
            if data['role'] not in ['user', 'admin', 'manager']:
                return jsonify({'error': 'Role inválido'}), 400
            user.role = data['role']

        if 'active' in data:
            user.active = data['active']

        try:
            db.session.commit()
            return jsonify(user.to_dict()), 200
        except:
            db.session.rollback()
            return jsonify({'error': 'Erro ao atualizar'}), 500

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        try:
            Task.query.filter_by(user_id=user_id).delete()
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'Usuário deletado com sucesso'}), 200
        except:
            db.session.rollback()
            return jsonify({'error': 'Erro ao deletar'}), 500

    @staticmethod
    def get_user_tasks(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        return jsonify([t.to_dict() for t in user.tasks]), 200

    @staticmethod
    def login():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({'error': 'Credenciais inválidas'}), 401

        if not user.active:
            return jsonify({'error': 'Usuário inativo'}), 403

        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': user.to_dict(),
            'token': f'jwt-token-{user.id}'
        }), 200
