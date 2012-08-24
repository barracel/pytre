from tre import tre

@tre
def _fib(n, a, b):
    if n == 0:
        return a
    else:
        return _fib(n - 1, a + b, a)

def fib(num):
    return _fib(num, 0, 1)


@tre
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


@tre
def even(n):
    if n == 0:
        return True
    else:
        return odd(n - 1)

@tre
def odd(n):
    if n == 0:
        return False
    else:
        return even(n - 1)


def compare_times():
    from timeit import Timer
    t1 = Timer("sum_recursive(1000)", "from __main__ import sum_recursive")
    t2 = Timer("sum_iterative(1000)", "from __main__ import sum_iterative")
    return (t1.timeit(number=1000), t2.timeit(number=1000))


if __name__ == '__main__':
    assert fib(1000) == 43466557686937456435688527675040625802564660517371780402481729089536555417949051890403879840079255169295922593080322634775209689623239873322471161642996440906533187938298969649928516003704476137795166849228875L
    assert sum_iterative(10000) == sum_recursive(10000)
    assert even(1000)
    assert not odd(1000)
    tr, ti = compare_times()
    print 'tre recursive is %.2f times slower than iterative' % (tr / ti)
