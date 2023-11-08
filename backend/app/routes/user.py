from datetime import datetime
from numbers import Integral
from flask import Blueprint, request, jsonify
from ..models import User, Card, Deck
from ..extensions import db
from ..util.auth import token_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/api/users', methods=['POST'])
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

    return jsonify({'data': new_user.get_json()}), 201


@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({'data': user.get_json()}), 200


@user_bp.route('/api/users', methods=['GET'])
def search_users():
    q = request.args.get('q')
    limit = request.args.get('limit')
    offset = request.args.get('offset')

    query = db.session.query(User)

    if q is not None:
        query = query.filter(User.username.ilike(f'%{q}%'))

    if limit is not None:
        try:
            limit = max(int(limit), 0)
        except:
            return jsonify({'message': 'Limit must be an integer'}), 400

        query = query.limit(limit)

        if offset is not None:
            try:
                offset = max(int(offset), 0)
            except:
                return jsonify({'message': 'Offset must be an integer'}), 400

            query = query.offset(offset)

    users = query.all()

    result = [user.get_json() for user in users]
    return jsonify({'data': result}), 200


@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(jwt_data, user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    request_user = db.session.get(User, jwt_data['user_id'])

    if not request_user:
        return jsonify({'message': 'Request user not found'}), 404

    if user.id != request_user.id and not request_user.admin:
        return jsonify({'message': 'You do not have the right to update this user'}), 403

    data = request.get_json()

    admin = data.get('admin')

    if admin:
        if not request_user.admin:
            return jsonify({'message': 'You do not have the right to update the "admin" field'}), 403

        user.admin = admin

    password = data.get('password')

    if password:
        current_password = data.get('current_password')

        if not current_password:
            return jsonify({'message': 'Please provide current password'}), 400

        if not user.check_password(current_password):
            return jsonify({'message': 'Provided password does not match with current password'}), 401

        user.set_password(password)

    username = data.get('username', user.username)
    user.username = username
    db.session.commit()

    return jsonify({'data': user.get_json()}), 200


@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(jwt_data, user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    request_user = db.session.get(User, jwt_data['user_id'])

    if not request_user:
        return jsonify({'message': 'Request user not found'}), 404

    if user.id != request_user.id and not request_user.admin:
        return jsonify({'message': 'You do not have the right to delete this user'}), 403

    db.session.delete(user)
    db.session.commit()

    return jsonify({'data': user.get_json()}), 200

# This actually creates a copy of the deck


@user_bp.route('/api/users/<int:user_id>/decks/<int:deck_id>', methods=['POST'])
@token_required
def add_deck(jwt_data, user_id, deck_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    request_user = db.session.get(User, jwt_data['user_id'])

    if not request_user:
        return jsonify({'message': 'Request user not found'}), 404

    if user.id != request_user.id and not request_user.admin:
        return jsonify({'message': 'You do not have the right to update this user'}), 403

    deck = db.session.get(Deck, deck_id)

    if not deck:
        return jsonify({'message': 'Deck not found'}), 404

    new_deck = Deck(name=deck.name, user=user)
    db.session.add(new_deck)
    db.session.commit()
    db.session.refresh(new_deck)

    db.session.add_all(Card(front=card.front, back=card.back,
                       deck=new_deck) for card in deck.cards)
    db.session.commit()

    return jsonify({'data': new_deck.get_json(cards_count='all,due,new')}), 201


@user_bp.route('/api/users/<int:user_id>/decks', methods=['GET'])
@token_required
def search_user_decks(jwt_data, user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    request_user = db.session.get(User, jwt_data['user_id'])

    if not request_user:
        return jsonify({'message': 'Request user not found'}), 404

    if user.id != request_user.id and not request_user.admin:
        return jsonify({'message': 'You do not have the right to view this user'}), 403

    q = request.args.get('q')
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    card_count = request.args.get('card_count')

    if card_count != None:
        card_count = card_count.split(',')

    query = Deck.query.filter(Deck.user_id == user.id)

    if q is not None:
        query = query.filter(Deck.name.ilike(f'%{q}%'))

    if limit is not None:
        try:
            limit = max(int(limit), 0)
        except:
            return jsonify({'message': 'Limit must be an integer'}), 400

        query = query.limit(limit)

        if offset is not None:
            try:
                offset = max(int(offset), 0)
            except:
                return jsonify({'message': 'Offset must be an integer'}), 400

            query = query.offset(offset)

    decks = query.all()

    data = [deck.get_json(card_count) for deck in decks]
    return jsonify({'data': data}), 200
