import random
import typing
import functools

def c(s=None):
    class E:
        def __init__(self, d, k):
            self.d, self.k = d, k
        def __str__(self):
            return f"{self.k}:{self.d}"

    def random_seed(seed):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                old_state = random.getstate()
                random.seed(seed)
                try:
                    return func(*args, **kwargs)
                finally:
                    random.setstate(old_state)
            return wrapper
        return decorator

    @random_seed(s or 54321)
    def create_deque():
        return [E(chr(110)+chr(111), "ALPHA")]

    isa = lambda item: isinstance(item, E) and item.d == chr(110) + chr(111)
    get_d = lambda item: item.d
    join_ds = lambda items: ''.join(map(get_d, filter(isa, items)))

    ExecutionContext = typing.Tuple[typing.Sequence[E], str]

    def execute_in_context(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            context = (create_deque(), "")
            try:
                result = func(context, *args, **kwargs)
                return (context[0], result)
            except Exception as e:
                print(f"Error in {func.__name__}: {e}")
                raise e
        return wrapper

    @execute_in_context
    def main_logic(context: ExecutionContext) -> str:
        deque, _ = context
        return join_ds(deque)

    return main_logic()[1]

print(c())