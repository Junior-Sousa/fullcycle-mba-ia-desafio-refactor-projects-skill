from flask import request, jsonify
from datetime import datetime, timezone
from src.database.connection import db
from src.models.task_model import Task
from src.models.user_model import User
from src.models.category_model import Category

class TaskController:
    @staticmethod
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([t.to_dict() for t in tasks]), 200

    @staticmethod
    def get_task(task_id):
        task = Task.query.get(task_id)
        if task:
            return jsonify(task.to_dict()), 200
        return jsonify({'error': 'Task não encontrada'}), 404

    @staticmethod
    def create_task():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400

        title = data.get('title')
        if not title:
            return jsonify({'error': 'Título é obrigatório'}), 400
        if len(title) < 3:
            return jsonify({'error': 'Título muito curto'}), 400
        if len(title) > 200:
            return jsonify({'error': 'Título muito longo'}), 400

        description = data.get('description', '')
        status = data.get('status', 'pending')
        priority = data.get('priority', 3)
        user_id = data.get('user_id')
        category_id = data.get('category_id')
        due_date = data.get('due_date')
        tags = data.get('tags')

        if status not in ['pending', 'in_progress', 'done', 'cancelled']:
            return jsonify({'error': 'Status inválido'}), 400
        if priority < 1 or priority > 5:
            return jsonify({'error': 'Prioridade deve ser entre 1 e 5'}), 400

        if user_id:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'Usuário não encontrado'}), 404

        if category_id:
            cat = Category.query.get(category_id)
            if not cat:
                return jsonify({'error': 'Categoria não encontrada'}), 404

        task = Task()
        task.title = title
        task.description = description
        task.status = status
        task.priority = priority
        task.user_id = user_id
        task.category_id = category_id

        if due_date:
            try:
                task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
            except:
                return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400

        if tags:
            task.tags = ','.join(tags) if isinstance(tags, list) else tags

        try:
            db.session.add(task)
            db.session.commit()
            return jsonify(task.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Erro ao criar task'}), 500

    @staticmethod
    def update_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task não encontrada'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400

        if 'title' in data:
            if len(data['title']) < 3:
                return jsonify({'error': 'Título muito curto'}), 400
            if len(data['title']) > 200:
                return jsonify({'error': 'Título muito longo'}), 400
            task.title = data['title']

        if 'description' in data:
            task.description = data['description']

        if 'status' in data:
            if data['status'] not in ['pending', 'in_progress', 'done', 'cancelled']:
                return jsonify({'error': 'Status inválido'}), 400
            task.status = data['status']

        if 'priority' in data:
            if data['priority'] < 1 or data['priority'] > 5:
                return jsonify({'error': 'Prioridade deve ser entre 1 e 5'}), 400
            task.priority = data['priority']

        if 'user_id' in data:
            if data['user_id']:
                user = User.query.get(data['user_id'])
                if not user:
                    return jsonify({'error': 'Usuário não encontrado'}), 404
            task.user_id = data['user_id']

        if 'category_id' in data:
            if data['category_id']:
                cat = Category.query.get(data['category_id'])
                if not cat:
                    return jsonify({'error': 'Categoria não encontrada'}), 404
            task.category_id = data['category_id']

        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
                except:
                    return jsonify({'error': 'Formato de data inválido'}), 400
            else:
                task.due_date = None

        if 'tags' in data:
            task.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']

        task.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

        try:
            db.session.commit()
            return jsonify(task.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Erro ao atualizar'}), 500

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task não encontrada'}), 404

        try:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deletada com sucesso'}), 200
        except:
            db.session.rollback()
            return jsonify({'error': 'Erro ao deletar'}), 500

    @staticmethod
    def search_tasks():
        query = request.args.get('q', '')
        status = request.args.get('status', '')
        priority = request.args.get('priority', '')
        user_id = request.args.get('user_id', '')

        tasks = Task.query

        if query:
            tasks = tasks.filter(
                db.or_(
                    Task.title.like(f'%{query}%'),
                    Task.description.like(f'%{query}%')
                )
            )

        if status:
            tasks = tasks.filter(Task.status == status)

        if priority:
            tasks = tasks.filter(Task.priority == int(priority))

        if user_id:
            tasks = tasks.filter(Task.user_id == int(user_id))

        return jsonify([t.to_dict() for t in tasks.all()]), 200

    @staticmethod
    def task_stats():
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        total = Task.query.count()
        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        cancelled = Task.query.filter_by(status='cancelled').count()

        overdue_count = Task.query.filter(
            Task.due_date.isnot(None),
            Task.due_date < now,
            Task.status.notin_(['done', 'cancelled'])
        ).count()

        stats = {
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'done': done,
            'cancelled': cancelled,
            'overdue': overdue_count,
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
        }

        return jsonify(stats), 200
