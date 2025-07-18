from typing import Any, Callable, TypeVar, Optional
from functools import wraps
import asyncio
import logging

T = TypeVar('T')

class RetryableError(Exception):
    pass

class ErrorHandler:
    @staticmethod
    async def retry_with_backoff(func: Callable[..., T], max_retries: int = 3, initial_delay: float = 1.0) -> T:
        delay = initial_delay
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                return await func()
            except RetryableError as e:
                last_exception = e
                if attempt < max_retries - 1:
                    await asyncio.sleep(delay)
                    delay *= 2
                continue
            except Exception as e:
                logging.error(f"Non-retryable error: {str(e)}")
                raise
        
        raise last_exception

def with_error_handling(max_retries: int = 3):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await ErrorHandler.retry_with_backoff(
                lambda: func(*args, **kwargs),
                max_retries=max_retries
            )
        return wrapper
    return decorator