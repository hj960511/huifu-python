from flask import Blueprint, jsonify, request
from model.user import User

api_users_bp = Blueprint('api_users', __name__)

@api_users_bp.route('/', methods=['GET'])
def get_users():
    users = User.get_all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users])

@api_users_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)
    user.save()
    return jsonify({"message": "用户已创建", "id": user.id}), 201


@api_users_bp.route('/get/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    return jsonify({"id": user.id, "name": user.name, "email": user.email})


@api_users_bp.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    data = request.get_json()
    user.update(**data)
    return jsonify({"message": "用户信息已更新"})


@api_users_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    user.delete()
    return jsonify({"message": "用户已删除"})
