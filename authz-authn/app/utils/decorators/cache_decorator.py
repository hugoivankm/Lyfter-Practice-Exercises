import json
from functools import wraps

from app.utils.cache import CacheManager
from flask import jsonify


def cache_response(key_prefix: str, timeout: int = 300):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_manager = CacheManager()
            # 1. Build un unique cache key
            cache_id = kwargs.get("id")
            key: str = f"{key_prefix}:{str(cache_id) if cache_id is not None else 'all'}"

            # 2. Try fetching from Redis
            cache_data = cache_manager.get_data(key)
            if cache_data is not None:
                try:
                    data, status_code = json.loads(cache_data)
                    if not isinstance(status_code, int):
                        raise TypeError("Invalid cache status code")
                    return jsonify(data), status_code
                except (json.JSONDecodeError, TypeError, ValueError):
                    print("warning: malformed json in response, deleting entry")
                    cache_manager.delete_data(key)

            # 3. Execute the actual route
            response = f(*args, **kwargs)

            # 4. Extract data and status code from Flask response -> only cache on success

            # We need to account the case where the reponse returns as object and not tuple
            if isinstance(response, tuple):
                response_obj, status_code = response[0], response[1]
            else:
                response_obj, status_code = response, 200

            if status_code == 200:
                data_to_cache = response_obj.get_json()
                serialized = json.dumps([data_to_cache, status_code])
                is_stored = cache_manager.store_data(key, serialized, timeout)
                if not is_stored:
                    print("warning: unable to save data to cache")

            return response

        return decorated_function

    return decorator
