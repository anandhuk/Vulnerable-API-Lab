from flask import request, jsonify
from functools import wraps
from app.services.storage import StorageService

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Auth-Token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        username = StorageService.validate_token(token)
        if not username:
            return jsonify({'message': 'Token is invalid!'}), 401

        # Add current user to request context
        request.current_user = username
        return f(*args, **kwargs)

    return decorated
