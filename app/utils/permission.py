from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify


def permission_role(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['sub']['role'] in roles:
                if claims['sub']['active'] == True:
                    return fn(*args, **kwargs)
                return jsonify(msg="Account is not active"), 403
            else:
                return jsonify(msg="Unauthorized for this user scope"), 403
        return decorator
    return wrapper