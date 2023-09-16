from flask import Blueprint, request, jsonify
from ..models import User
from ..extensions import db
from ..util.auth import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_data = {
        'id': user.id,
        'username': user.username,
    }
    return jsonify(user_data), 200

@user_bp.route('/users/search', methods=['GET'])
def search_users():
    query = request.args.get('q')

    if not query:
        return jsonify({'message': 'Please provide a search query'}), 400

    users = User.query.filter(User.username.ilike(f'%{query}%')).all()

    if not users:
        return jsonify({'message': 'No users found for the given query'}), 404

    result = [{'id': user.id, 'username': user.username} for user in users]

    return jsonify(result), 200

@user_bp.route('/user', methods=['PUT'])
@token_required
def update_user(jwt_data):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    new_username = data.get('username')

    if new_username is None:
        return jsonify({'message': 'Username is required for updating'}), 400

    user.username = new_username
    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200

@user_bp.route('/user', methods=['DELETE'])
@token_required
def delete_user(jwt_data):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200
