from flask import Blueprint, request, jsonify, current_app
from ..models import Deck, Card, User
from ..extensions import db
from ..util.auth import token_required

card_bp = Blueprint('card', __name__)

@card_bp.route('/decks/<int:deck_id>/cards', methods=['POST'])
@token_required
def create_card(jwt_data, deck_id):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    deck = db.session.get(Deck, deck_id)

    if not deck:
        return jsonify({'message': 'Deck not found'}), 404

    if deck.user_id != user.id:
        return jsonify({'message': 'You do not own this deck'}), 403

    data = request.json
    front = data.get('front')
    back = data.get('back')
    reverse = data.get('reverse') or False

    if not front or not back:
        return jsonify({'message': 'Please provide card front and back'}), 400

    card = Card(front=front, back=back, deck=deck)
    db.session.add(card)
    db.session.commit()
    data = [card.get_json()]

    if reverse:
        reverse_card = Card(front=back, back=front, deck=deck)
        db.session.add(reverse_card)
        db.session.commit()
        data.append(reverse_card.get_json())

    return jsonify({'message': 'Cards created successfully', 'data': data}), 201

@card_bp.route('/decks/<int:deck_id>/cards', methods=['GET'])
@token_required
def search_cards(jwt_data, deck_id):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    deck = db.session.get(Deck, deck_id)

    if not deck:
        return jsonify({'message': 'Deck not found'}), 404
    if not deck.shared and deck.user_id != user.id:
        return jsonify({'message': 'You do not own this deck'}), 403

    q = request.args.get('q')
    limit = request.args.get('limit')
    offset = request.args.get('offset')

    query = Card.query.filter(Card.deck_id == deck.id)

    if q:
        query = query.filter(Card.front.ilike(f'%{q}%'))

    if limit:
        query = query.limit(limit)

        if offset:
            query = query.offset(offset)

    cards = query.all()

    card_list = [card.get_json() for card in cards]
    return jsonify({'data': card_list}), 200

@card_bp.route('/cards/<int:card_id>', methods=['GET'])
@token_required
def get_card(jwt_data, card_id):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    card = db.session.get(Card, card_id)

    if not card:
        return jsonify({'message': 'Card not found'}), 404

    if not card.deck.shared and card.deck.user_id != user.id:
        return jsonify({'message': 'You do not have the deck to which this card pertains'}), 403

    return jsonify({'data': card.get_json()}), 200

@card_bp.route('/cards/<int:card_id>', methods=['PUT'])
@token_required
def update_card(jwt_data, card_id):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    card = db.session.get(Card, card_id)

    if not card:
        return jsonify({'message': 'Card not found'}), 404

    if card.deck.user_id != user.id:
        return jsonify({'message': 'You do not have permission to update this card'}), 403

    data = request.json
    front = data.get('front', card.front)
    back = data.get('back', card.back)

    card.front = front
    card.back = back
    db.session.commit()

    return jsonify({'message': 'Card updated successfully', 'data': card.get_json()}), 200

@card_bp.route('/cards/<int:card_id>', methods=['DELETE'])
@token_required
def delete_card(jwt_data, card_id):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    card = db.session.get(Card, card_id)

    if not card:
        return jsonify({'message': 'Card not found'}), 404

    if card.deck.user_id != user.id:
        return jsonify({'message': 'You do not have permission to delete this card'}), 403

    db.session.delete(card)
    db.session.commit()

    return jsonify({'message': 'Card deleted successfully', 'data': card.get_json()}), 200
