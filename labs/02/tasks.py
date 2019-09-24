def fizzbuzz(num):
    """
    1 point.
    Return 'Fizz' if `num` is divisible by 3, 'Buzz' if `num` is divisible by 5, 'FizzBuzz' if `num` is divisible both by 3 and 5.
    If `num` isn't divisible neither by 3 nor by 5, return `num`.
    Example:
        fizzbuzz(3) # Fizz
        fizzbuzz(5) # Buzz
        fizzbuzz(15) # FizzBuzz
        fizzbuzz(8) # 8
    """
    pass


def fibonacci(n):
    """
    1 point
    Return the `n`-th Fibonacci number (counting from 0).
    Example:
        fibonacci(0) == 0
        fibonacci(1) == 1
        fibonacci(2) == 1
        fibonacci(3) == 2
        fibonacci(4) == 3
    """
    pass


def dot_product(a, b):
    """
    1 point
    Calculate the dot product of `a` and `b`.
    Assume that `a` and `b` have same length.
    Hint:
        lookup `zip` function
    Example:
        dot_product([1, 2, 3], [0, 3, 4]) == 1*0 + 2*3 + 3*4 == 18
    """
    pass


def redact(data, chars):
    """
    1 point
    Return `data` with all characters from `chars` replaced by the character 'x'.
    Characters are case sensitive.
    Example:
        redact("Hello world!", "lo")        # Hexxx wxrxd!
        redact("Secret message", "mse")     # Sxcrxt xxxxagx
    """
    pass


def count_words(data):
    """
    1 point
    Return a dictionary that maps word -> number of occurences in `data`.
    Words are separated by spaces (' ').
    Characters are case sensitive.

    Hint:
        "hi there".split(" ") -> ["hi", "there"]

    Example:
        count_words('this car is my favourite what car is this')
        {
            'this': 2,
            'car': 2,
            'is': 2,
            'my': 1,
            'favourite': 1,
            'what': 1
        }
    """
    pass


def bonus_fizzbuzz(num):
    """
    1 point (bonus)
    Implement the `fizzbuzz` function.
    `if` and cycles are not allowed.
    """
    pass


def bonus_utf8(cp):
    """
    1 point (bonus)
    Encode `cp` (a Unicode code point) into 1-4 UTF-8 bytes - you should know this from `Logické obvody`.
    Example:
        bonus_utf8(0x01) == [0x01]
        bonus_utf8(0x1F601) == [0xF0, 0x9F, 0x98, 0x81]
    """
    pass
