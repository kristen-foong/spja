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
    if num % 3 == 0 and num % 5 == 0:
        return "FizzBuzz"
    if num % 3 == 0:
        return "Fizz"
    if num % 5 == 0:
        return "Buzz"
    return num


def fibonacci(n):
    """
    1 point
    Return `n`th Fibonacci number (counting from 0).
    Example:
        fibonacci(0) == 0
        fibonacci(1) == 1
        fibonacci(2) == 1
        fibonacci(3) == 2
        fibonacci(4) == 3
    """
    if n == 0:
        return 0
    if n < 3:
        return 1
    return fibonacci(n - 2) + fibonacci(n - 1)


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
    return sum(x * y for (x, y) in zip(a, b))


def redact(data, chars):
    """
    1 point
    Return `data` with all characters from `chars` replaced by the character 'x'.
    Characters are case sensitive.
    Example:
        redact("Hello world!", "lo")        # Hexxx wxrxd!
        redact("Secret message", "mse")     # Sxcrxt xxxxagx
    """
    result = ""
    for d in data:
        if d in chars:
            result += "x"
        else:
            result += d
    return result


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
    words = data.split(" ")
    count = {}
    for word in words:
        if word:
            if word not in count:
                count[word] = 0
            count[word] += 1
    return count


def bonus_fizzbuzz(num):
    """
    1 point (bonus)
    Implement the `fizzbuzz` function without using any conditional operation or condition.
    `if` and cycles are not allowed.
    """
    l = ["Fizz", "", ""]
    r = ["Buzz", "", "", "", ""]
    l = l[num % 3]
    r = r[num % 5]
    res = l + r
    return {
        True: num,
        False: res
    }[res == ""]


def bonus_utf8(cp):
    """
    1 point (bonus)
    Encode `cp` (a Unicode code point) into 1-4 UTF-8 bytes - you should know this from `Logické obvody`.
    Example:
        bonus_utf8(0x01) == [0x01]
        bonus_utf8(0x1F601) == [0xF0, 0x9F, 0x98, 0x81]
    """
    import math

    def comp(bits):
        num = cp
        res = []
        byte_count = math.ceil(bits / 6)

        while bits >= 6:
            res.append(0x80 | (num & 0b00111111))
            num >>= 6
            bits -= 6

        if bits:
            s = 0xC0
            mask = 0b00100000
            for _ in range(byte_count - 2):
                s |= mask
                mask >>= 1
            s |= num & ((1 << bits) - 1)
            res.append(s)

        return reversed(res)

    if cp <= 0x7F:
        return [cp]
    elif cp <= 0x7FF:
        return comp(11)
    elif cp <= 0xFFFF:
        return comp(16)
    elif cp <= 0x1FFFFF:
        return comp(21)
