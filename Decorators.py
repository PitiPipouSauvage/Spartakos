from functools import wraps
from time import perf_counter

def get_time(func):
    """Times any function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()

        func(*args, *kwargs)

        end_time = perf_counter()
        total_time = round(end_time - start_time, 50)

        print(f'Time {total_time} seconds')

    return wrapper
