def incrementor(n):
    """
    1 point
    Return a function that will add `n` to its parameter.
    If this function receives no parameter, it should create an incrementor that adds 1 to its parameter.
    Example:
        inc = incrementor(5)
        inc(6) # 11
        inc(1) # 6

        inc = incrementor()
        inc(2) # 3
    """
    pass


def fibonacci_closure():
    """
    2 points
    Return a closure that will generate elements of the Fibonacci sequence when called repeatedly.
    Example:
        g = fibonacci_closure()
        g() # 1
        g() # 1
        g() # 2
        g() # 3
        ...
    """
    pass


def prime_generator():
    """
    2 points
    Return a generator that will generate prime numbers when iterated.
    Example:
        for i in prime_generator():
            print(i)
        # 2, 3, 5, 7, 11, 13 ...
    """
    pass


def transform_file(src, dst, keyword):
    """
    2 points
    Open file located at `src`, keep only lines that contain the `keyword`, sort them in ascending
    order and write them to file located at `dst`.

    If `src` does not exist, return "file not found".
    If everything goes ok, return "ok".

    Example:
        transform_file('in.txt', 'out.txt', 'or')

        in.txt:
        barrens
        stormwind
        gondor
        ashenvale
        hogwarts
        yavin
        coruscant

        out.txt:
        coruscant
        gondor
        stormwind
    """
    pass


def cached(f):
    """
    2 points
    Create a decorator that caches the latest function result.
    When `f` is called multiple times in a row with the same parameter, compute the result just
    once and then return the result from cache.
    When `f` receives a different parameter, reset the cache and compute a new result.
    Assume that `f` receives exactly one parameter.
    Example:
        @cached
        def fn(a):
            return a + 1 # imagine an expensive computation

        fn(1) == 2 # computed
        fn(1) == 2 # returned from cache, `a + 1` is not executed
        fn(3) == 4 # computed
        fn(1) == 2 # computed
    """
    pass


def bonus_tree_walker(tree, order):
    """
    1 point (bonus)
    Write a generator that traverses `tree` in the given `order` ('inorder', 'preorder' or 'postorder').
    You should know this from 'Algoritmy II'.
    The tree is represented with nested tuples (left subtree, value, right subtree).
    If there is no subtree, it will be marked as None.
    Example:
        tree = (((None, 8, None), 3, (None, 4, None)), 5, (None, 1, None))
            5
           / \
          3   1
         / \
        8   4
        list(bonus_tree_walker(tree, 'inorder')) == [8, 3, 4, 5, 1]
        list(bonus_tree_walker(tree, 'preorder')) == [5, 3, 8, 4, 1]
        list(bonus_tree_walker(tree, 'postorder')) == [8, 4, 3, 1, 5]
    """
    pass
