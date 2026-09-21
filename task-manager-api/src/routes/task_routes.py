from flask import Blueprint
from src.controllers.task_controller import TaskController

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    return TaskController.get_tasks()

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    return TaskController.get_task(task_id)

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    return TaskController.create_task()

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    return TaskController.update_task(task_id)

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    return TaskController.delete_task(task_id)

@task_bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    return TaskController.search_tasks()

@task_bp.route('/tasks/stats', methods=['GET'])
def task_stats():
    return TaskController.task_stats()
