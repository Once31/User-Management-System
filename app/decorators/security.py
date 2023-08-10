from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt

from flask import request

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            print(claims)
            if claims['role'] == 'ADMIN':
                return fn(*args, **kwargs)
            return {'msg':'adming only'}, 403
        
        return decorator
    return wrapper


def admin_or_self_required(user_id_param = 'id'):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            request_user_id = request.view_args.get(user_id_param)
            print(f'request user id [{user_id_param}]')
            
            if claims['role'] == 'ADMIN' or (request_user_id is not None and request_user_id == claims['user_id']):
                return fn(*args, **kwargs)
            return {'msg': 'ADMIN ONLY!'}, 403
        return decorator
    
    return wrapper