from functools import wraps
from utils.decorators import cache_decorator

def cache_response(key_prefix: str, timeout:int = 300):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            