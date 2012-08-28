from timeit import Timer
import contextlib

from tre import tre, tre_safe

def mark_tre(func):
    func._tre = True
    return func

@mark_tre
def _fib(n, a, b):
    if n == 0:
        return a
    else:
        return _fib(n - 1, a + b, a)

def fib(num):
    return _fib(num, 0, 1)

@mark_tre
def _sum_recursive(n, accum):
    if n <= 1:
        return accum + 1
    else:
        return _sum_recursive(n - 1, n + accum)

def sum_recursive(n):
    return _sum_recursive(n, 0)

def sum_iterative(n):
    acum = 0
    while n:
        acum += n
        n -= 1
    return acum

@mark_tre
def even(n):
    if n == 0:
        return True
    else:
        return odd(n - 1)
@mark_tre
def odd(n):
    if n == 0:
        return False
    else:
        return even(n - 1)


def compare_times(decorator):
    name = decorator.func_name
    setup = ("from __main__ import tre_decorator, sum_recursive, sum_iterative"
             ", _sum_recursive, %s" % name)
    t1 = Timer("with tre_decorator(%s):sum_recursive(1000)" % name, setup)
    t2 = Timer("with tre_decorator(%s):sum_iterative(1000)" % name, setup)
    return (t1.timeit(number=1000), t2.timeit(number=1000))

@contextlib.contextmanager
def tre_decorator(decorator):
    originals = dict((name, func) for name, func in globals().items()
                     if getattr(func, '_tre', False))

    for name, func in originals.items():
        globals()[name] = decorator(func)

    try:
        yield
    finally:
        for name, func in originals.items():
            globals()[name] = func

def run_tests():
    assert fib(1000) == 43466557686937456435688527675040625802564660517371780402481729089536555417949051890403879840079255169295922593080322634775209689623239873322471161642996440906533187938298969649928516003704476137795166849228875L
    assert sum_iterative(10000) == sum_recursive(10000)
    assert even(1000)
    assert not odd(1000)

if __name__ == '__main__':
    for decorator in (tre, tre_safe):
        with tre_decorator(decorator):
            run_tests()
            compare_times(decorator)
            tr, ti = compare_times(decorator)
            print ('%s is %.2f times slower than iterative'
                   % (decorator.func_name, (tr / ti)))
