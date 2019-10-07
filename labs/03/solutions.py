import math
from functools import wraps


def transform_file(src, dst, keyword):
    try:
        with open(src, "r") as f:
            lines = sorted([l.strip() for l in f if keyword in l])
        with open(dst, "w") as d:
            d.writelines("\n".join(lines))
    except FileNotFoundError:
        return 'file not found'

    return 'ok'


def incrementor(n=1):
    return lambda x: x + n


def fibonacci_closure():
    data = []
    # or you could use two variables and refer to them using `nonlocal`

    def fn():
        if not data:
            data.extend((0, 1))
            return 1

        next = sum(data)
        data[0], data[1] = data[1], next
        return next
    return fn


def prime_generator():
    yield 2

    prime = 3
    while True:
        yield prime

        while True:
            prime += 2
            if all(prime % divisor != 0 for divisor in range(3, int(math.sqrt(prime)) + 1)):
                break


def cached(f):
    params = []
    cached = None

    # functools.wraps keeps the wrapped function's name and documentation
    @wraps(f)
    def fn(*args):
        nonlocal params, cached

        # you should check whether this is the first call
        # pre-setting cache to None or 0 may not work if the inner function
        # really receives None or 0 as a parameter
        if params and params == args:
            return cached
        params = args
        cached = f(*args)
        return cached

    return fn


def bonus_tree_walker(tree, order):
    if not tree:
        return

    l, v, r = tree

    if order == 'inorder':
        yield from bonus_tree_walker(l, order)
        yield v
        yield from bonus_tree_walker(r, order)
    elif order == 'preorder':
        yield v
        yield from bonus_tree_walker(l, order)
        yield from bonus_tree_walker(r, order)
    else:
        yield from bonus_tree_walker(l, order)
        yield from bonus_tree_walker(r, order)
        yield v
