from flask import Blueprint, request, jsonify, current_app
from ..models import Deck, User
from ..extensions import db
from ..util.auth import token_required

deck_bp = Blueprint('deck', __name__)

@deck_bp.route('/decks', methods=['POST'])
@token_required
def create_deck(jwt_data):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'message': 'Deck name is required'}), 400

    deck = Deck(name=name, user=user)
    db.session.add(deck)
    db.session.commit()

    return jsonify({'data': deck.get_json()}), 201

@deck_bp.route('/decks/<int:deck_id>', methods=['GET'])
@token_required
def get_deck(jwt_data, deck_id):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    deck = db.session.get(Deck, deck_id)

    if not deck:
        return jsonify({'message': 'Deck not found'}), 404

    if not deck.shared and deck.user_id != user.id:
        return jsonify({'message': 'You do not own this deck'}), 403

    return jsonify(deck.get_json()), 200

@deck_bp.route('/decks/<int:deck_id>', methods=['PUT'])
@token_required
def update_deck(jwt_data, deck_id):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    deck = db.session.get(Deck, deck_id)

    if not deck:
        return jsonify({'message': 'Deck not found'}), 404

    if deck.user_id != user.id:
        return jsonify({'message': 'You do not own this deck'}), 403

    data = request.json

    name = data.get('name', deck.name)
    shared = data.get('shared', False)

    deck.name = name
    deck.shared = shared
    db.session.commit()

    return jsonify({'data': deck.get_json()}), 200

@deck_bp.route('/decks/<int:deck_id>', methods=['DELETE'])
@token_required
def delete_deck(jwt_data, deck_id):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    deck = db.session.get(Deck, deck_id)

    if not deck:
        return jsonify({'message': 'Deck not found'}), 404

    if deck.user_id != user.id:
        return jsonify({'message': 'You do not own this deck'}), 403

    data = deck.get_json()
    db.session.delete(deck)
    db.session.commit()

    return jsonify({'data': data}), 200

@deck_bp.route('/decks', methods=['GET'])
def search_decks():
    q = request.args.get('q')
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    count = request.args.get('count')

    query = Deck.query.filter(Deck.shared == True)

    if q:
        query = query.filter(Deck.name.ilike(f'%{q}%'))

    if limit:
        query = query.limit(limit)

        if offset:
            query = query.offset(offset)

    if count:
        return jsonify({'data': query.count()}), 200

    decks = query.all()

    deck_list = [deck.get_json() for deck in decks]
    return jsonify({'data': deck_list}), 200
