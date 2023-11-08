from flask import Blueprint, send_from_directory, send_file

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/', methods=['GET'])
def index(): # pragma: no cover
    return send_file('../frontend/index.html')

@frontend_bp.route('/<path:name>', methods=['GET'])
def frontend(name): # pragma: no cover
    return send_from_directory('../frontend', name)
