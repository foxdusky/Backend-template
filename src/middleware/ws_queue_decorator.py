from functools import wraps

from ws import ws_manager


def ws_queue(queue_name: str):
    def decorator(func):
        # * @wraps(func) - prevent overwriting endpoint docs
        @wraps(func)
        async def wrapper(*args, **kwargs):
            response = await func(*args, **kwargs)

            # Send msg to frontend to update/refetch cache by queue name
            await ws_manager.broadcast(queue_name)

            return response

        return wrapper

    return decorator

