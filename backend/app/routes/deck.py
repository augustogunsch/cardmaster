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

    deck = Deck(name=name, owner=user)
    db.session.add(deck)
    db.session.commit()

    return jsonify({'message': 'Deck created successfully'}), 201

@deck_bp.route('/decks/<int:deck_id>', methods=['GET'])
@token_required
def get_deck(jwt_data, deck_id):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    deck = db.session.get(Deck, deck_id)

    if not deck:
        return jsonify({'message': 'Deck not found'}), 404

    if deck.shared or deck.owner == user:
        return jsonify({'id': deck.id, 'name': deck.name, 'owner': deck.owner.username}), 200

@deck_bp.route('/decks/<int:deck_id>', methods=['PUT'])
@token_required
def update_deck(jwt_data, deck_id):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    deck = db.session.get(Deck, deck_id)

    if not deck:
        return jsonify({'message': 'Deck not found'}), 404

    if deck.owner != user:
        return jsonify({'message': 'You do not have permission to update this deck'}), 403

    data = request.json

    name = data.get('name') or deck.name
    shared = data.get('shared') or deck.shared

    deck.name = name
    deck.shared = shared
    db.session.commit()

    return jsonify({'message': 'Deck updated successfully'}), 200

@deck_bp.route('/decks/<int:deck_id>', methods=['DELETE'])
@token_required
def delete_deck(jwt_data, deck_id):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    deck = db.session.get(Deck, deck_id)

    if not deck:
        return jsonify({'message': 'Deck not found'}), 404

    if deck.owner != user:
        return jsonify({'message': 'You do not have permission to delete this deck'}), 403

    db.session.delete(deck)
    db.session.commit()

    return jsonify({'message': 'Deck deleted successfully'}), 200

@deck_bp.route('/decks/shared', methods=['GET'])
def get_shared_decks():
    query = request.args.get('query')

    if query:
        decks = Deck.query.filter(Deck.shared.is_(True), Deck.name.ilike(f'%{query}%')).all()
    else:
        decks = Deck.query.filter_by(shared=True).all()

    deck_list = [{'id': deck.id, 'name': deck.name} for deck in decks]
    return jsonify(deck_list), 200

@deck_bp.route('/decks/owned', methods=['GET'])
@token_required
def get_owned_decks(jwt_data):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    owned_decks = [{'id': deck.id, 'name': deck.name} for deck in user.decks_owned]
    return jsonify(owned_decks), 200

@deck_bp.route('/decks', methods=['GET'])
@token_required
def get_collected_decks(jwt_data):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user.decks), 200

@deck_bp.route('/decks/add/<int:deck_id>', methods=['POST'])
@token_required
def add_deck_to_collection(jwt_data, deck_id):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    deck = db.session.get(Deck, deck_id)

    if not deck:
        return jsonify({'message': 'Deck not found'}), 404

    user.decks.append(deck)
    db.session.commit()

    return jsonify({'message': 'Deck added to your collection'}), 200
