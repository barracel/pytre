import collections
import contextlib
import functools
import threading

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

def tre_global(func):
    def wraps(*args, **kwargs):
        with recursive_identity(func) as ri:
            res = (args, kwargs)
            while ri['called']:
                ri['called'] = False
                res = func(*res[0], **res[1])
            return res
    return wraps


Call = collections.namedtuple('Call', ('func', 'args', 'kwargs'))

_local = threading.local()
_local.tre = {'trampoline': False, 'call': False}

def tre_trampoline(func):
    @functools.wraps(func)
    def wraps(*args, **kwargs):
        if not _local.tre['trampoline']:
            _local.tre['trampoline'] = True
            obj = Call(func, args, kwargs)
            while isinstance(obj, Call):
                obj = obj.func(*obj.args, **obj.kwargs)
            _local.tre['trampoline'] = False
            return obj
        else:
            if _local.tre['call']:
                _local.tre['call'] = False
                return Call(func, args, kwargs)
            else:
                _local.tre['call'] = True
                return func(*args, **kwargs)
    return wraps
