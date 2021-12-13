from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify


def only_role(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            print(claims)
            if role in claims['sub']['role']:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Unauthorized for this user scope"), 403
        return decorator
    return wrapper