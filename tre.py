import functools
import contextlib

@contextlib.contextmanager
def recursive_identity(func):
    called = dict(called=True)

    def identity(*args, **kwargs):
        called['called'] = True
        return (args, kwargs)

    original = func.__globals__[func.__name__]
    try:
        func.__globals__[func.__name__] = identity
        yield called
    finally:
        func.__globals__[func.__name__] = original

def tre(func):
    @functools.wraps(func)
    def wraps(*args, **kwargs):
        with recursive_identity(func) as ri:
            res = (args, kwargs)
            while ri['called']:
                ri['called'] = False
                res = func(*res[0], **res[1])
            return res
    return wraps
