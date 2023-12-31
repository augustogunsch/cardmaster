from flask import Blueprint, request, jsonify, current_app
import jwt
from ..models import User
from ..extensions import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/auth', methods=['POST'])
def auth():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Summing this value to current UTC
    # time should result in the user's time.
    # It should be measured in SECONDS.
    tzutcdelta = data.get('tzutcdelta')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if tzutcdelta == None:
        return jsonify({'message': 'Field "tzutcdelta" is required'}), 400

    try:
        tzutcdelta = int(tzutcdelta)
    except:
        return jsonify({'message': 'Field "tzutcdelta" must be a timezone delta in seconds'}), 400

    user = User.query.filter(User.username == username).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.check_password(password):
        user.tzutcdelta = tzutcdelta
        db.session.commit()
        payload = {'user_id': user.id}
        token = jwt.encode(
            payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token.decode('utf-8'), 'user': user.get_json()})
    else:
        return jsonify({'message': 'Authentication failed'}), 401
