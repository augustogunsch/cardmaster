from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from ..models import Deck, User
from ..extensions import db
from ..util.auth import token_required

deck_bp = Blueprint('deck', __name__)


@deck_bp.route('/api/decks', methods=['POST'])
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


@deck_bp.route('/api/decks/<int:deck_id>', methods=['GET'])
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

    card_count = request.args.get('card_count')

    if card_count != None:
        card_count = card_count.split(',')

    return jsonify({
        'data': deck.get_json(card_count, tzutcdelta=user.tzutcdelta)
    }), 200


@deck_bp.route('/api/decks/<int:deck_id>', methods=['PUT'])
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


@deck_bp.route('/api/decks/<int:deck_id>', methods=['DELETE'])
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


@deck_bp.route('/api/decks', methods=['GET'])
def search_decks():
    q = request.args.get('q')
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    total_count = request.args.get('total_count') != None
    card_count = request.args.get('card_count')

    if card_count != None:
        card_count = card_count.split(',')

    query = Deck.query.filter(Deck.shared == True)

    if q is not None:
        query = query.filter(Deck.name.ilike(f'%{q}%'))

    if total_count:
        total_count = query.count()

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

    deck_list = [deck.get_json(card_count) for deck in decks]

    data = {'data': deck_list}

    if total_count:
        data['count'] = total_count

    return jsonify(data), 200
