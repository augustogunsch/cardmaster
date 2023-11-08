from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from ..models import Deck, Card, User
from ..extensions import db
from ..util.auth import token_required
from ..util import date

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
    count = request.args.get('count') != None
    new = request.args.get('new') != None
    due = request.args.get('due')
    revised = request.args.get('revised')

    query = Card.query.filter(Card.deck_id == deck.id)

    if new:
        query = query.filter(Card.knowledge_level == 0)

    if due:
        try:
            due = date.normalize(datetime.fromisoformat(due))
        except:
            return jsonify({'message': 'Field "due" must be an isoformat date'}), 400

        query = query.filter(Card.revision_due <= due)

    if revised:
        try:
            revised = date.normalize(datetime.fromisoformat(revised)).date()
        except:
            return jsonify({'message': 'Field "revised" must be an isoformat date'}), 400

        query = query.filter(Card.last_revised == revised)

    if q is not None:
        query = query.filter(Card.front.ilike(f'%{q}%'))

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

    if count:
        return jsonify({'data': query.count()}), 200

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
    knowledge_level = data.get('knowledge_level', card.knowledge_level)
    last_revised = data.get('last_revised', card.last_revised)
    revision_due = data.get('revision_due', card.revision_due)

    if last_revised != None:
        try:
            card.last_revised = date.normalize(
                datetime.fromisoformat(last_revised))
        except:
            return jsonify({'message': 'Field "last_revised" must be an isoformat date'}), 400

    if revision_due != None:
        try:
            card.revision_due = date.normalize(
                datetime.fromisoformat(revision_due))
        except:
            return jsonify({'message': 'Field "revision_due" must be an isoformat date'}), 400

    if knowledge_level != None:
        try:
            card.knowledge_level = int(knowledge_level)
        except:
            return jsonify({'message': 'Field "knowledge_level" must be an integer'}), 400

    card.front = front
    card.back = back

    db.session.commit()

    return jsonify({'message': 'Card updated successfully', 'data': card.get_json()}), 200


@card_bp.route('/cards', methods=['PUT'])
@token_required
def update_cards(jwt_data):
    user = db.session.get(User, jwt_data['user_id'])

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json

    if not isinstance(data, list):
        return jsonify({'message': 'Expected a list as body'}), 400

    for new_card in data:
        id = new_card.get('id')

        if not id:
            return jsonify({'message': 'Missing id field'}), 400

        card = db.session.get(Card, id)

        if not card:
            return jsonify({'message': 'Card with id {} not found'.format(id)}), 404

        if card.deck.user_id != user.id:
            return jsonify({'message': 'You do not have permission to update card with id {}'.format(id)}), 403

        front = new_card.get('front', card.front)
        back = new_card.get('back', card.back)
        knowledge_level = new_card.get('knowledge_level', card.knowledge_level)
        last_revised = new_card.get('last_revised', card.last_revised)
        revision_due = new_card.get('revision_due', card.revision_due)

        if last_revised != None:
            try:
                card.last_revised = date.normalize(
                    datetime.fromisoformat(last_revised))
            except:
                return jsonify({'message': 'Field "last_revised" must be an isoformat date'}), 400

        if revision_due != None:
            try:
                card.revision_due = date.normalize(
                    datetime.fromisoformat(revision_due))
            except:
                return jsonify({'message': 'Field "revision_due" must be an isoformat date'}), 400

        if knowledge_level != None:
            try:
                card.knowledge_level = int(knowledge_level)
            except:
                return jsonify({'message': 'Field "knowledge_level" must be an integer'}), 400

        card.front = front
        card.back = back

    db.session.commit()

    return jsonify({'message': 'Cards updated successfully'}), 200


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
