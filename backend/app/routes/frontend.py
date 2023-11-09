from flask import Blueprint, send_from_directory, send_file

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/', defaults={'name': ''}, methods=['GET'])
@frontend_bp.route('/<path:name>', methods=['GET'])
def index(name): # pragma: no cover
    return send_file('../frontend/index.html')

@frontend_bp.route('/favicon.svg', methods=['GET'])
def favicon(): # pragma: no cover
    return send_file('../frontend/favicon.svg')

@frontend_bp.route('/assets/<path:name>', methods=['GET'])
def frontend(name): # pragma: no cover
    return send_from_directory('../frontend/assets', name)
