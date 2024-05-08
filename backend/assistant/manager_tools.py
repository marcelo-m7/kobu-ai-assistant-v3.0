import json
from tenacity import retry, wait_random_exponential, stop_after_attempt


class ManagerTools:
    RETRY = lambda: retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))

    @classmethod
    def debugger_exception_decorator(cls, func):
        """Wrap the function in a try flow, where the Exception is printed."""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"{func.__name__} Error: {e}")
        return wrapper
    
    """
    @classmethod
    def retry_decorator(cls, func):
        # ""Retry decorator for retrying operations.""
        @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"{func.__name__} Error: {e}")
                raise e
        return wrapper
    """
