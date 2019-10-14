import itertools
import time


class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, rhs):
        if not isinstance(rhs, Vector):
            raise ValueError()
        return Vector(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)

    def __sub__(self, rhs):
        if not isinstance(rhs, Vector):
            raise ValueError()
        return Vector(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)

    def __eq__(self, rhs):
        if not isinstance(rhs, Vector):
            return False
        return self.x == rhs.x and self.y == rhs.y and self.z == rhs.z

    def __getitem__(self, index):
        return (self.x, self.y, self.z)[index]

    def __setitem__(self, index, val):
        if index == 0:
            self.x = val
        elif index == 1:
            self.y = val
        elif index == 2:
            self.z = val
        else:
            raise IndexError()

        """
        or replace conditions with table lookup:
        mapping = {
            0: 'x',
            1: 'y',
            2: 'z'
        }
        self.__dict__[mapping[index]] = val
        """

    def __iter__(self):
        for attribute in (self.x, self.y, self.z):
            yield attribute
        """
        or
        yield from iter((self.x, self.y, self.z))
        or simply
        yield self.x
        yield self.y
        yield self.z
        """

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)


class UpperCaseDecorator:
    def __init__(self, f):
        self.f = f

    def write(self, data):
        self.f.write(self._transform(data))

    def writelines(self, lines):
        self.f.writelines(self._transform(l) for l in lines)

    def _transform(self, line):
        return "".join([c.upper() for c in line if not c.isupper()])


class Observable:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

        def rm():
            if subscriber in self.subscribers:
                self.subscribers.remove(subscriber)
        return rm

    def notify(self, *args, **kwargs):
        for s in self.subscribers:
            s(*args, **kwargs)


class GameOfLife:
    NEIGHBOUR_COUNT = 8
    ALIVE = 'x'
    DEAD = '.'

    def __init__(self, board):
        self.board = board

    @property
    def width(self):
        return len(self.board[0])

    @property
    def height(self):
        return len(self.board)

    def move(self):
        board = tuple(list(row) for row in self.board)

        """
        enumerate takes an iterable and returns tuples
        (0, first element from iterable)
        (1, second element from iterable)
        (2, third element from iterable)
        useful for obtaining indices of iterated elements
        """
        for row, line in enumerate(self.board):
            for col, character in enumerate(line):
                neighbours = tuple(self.get_neighbours(row, col))
                dead = (GameOfLife.NEIGHBOUR_COUNT - len(neighbours)) + len(tuple(n for n in neighbours if n == GameOfLife.DEAD))
                alive = GameOfLife.NEIGHBOUR_COUNT - dead
                status = GameOfLife.ALIVE
                if character == GameOfLife.ALIVE and (alive < 2 or alive > 3):
                    status = GameOfLife.DEAD
                elif character == GameOfLife.DEAD and alive != 3:
                    status = GameOfLife.DEAD
                board[row][col] = status
        return GameOfLife(tuple(tuple(row) for row in board))

    def get_neighbours(self, row, col):
        def inside(x, y):
            return 0 <= x < self.height and 0 <= y < self.width

        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if inside(row + x, col + y) and (x, y) != (0, 0):
                    yield self.board[row + x][col + y]
        """
        or
        for (x, y) in itertools.product((-1, 0, 1), (-1, 0, 1)):
            ...
        """

    def alive(self):
        # itertools.chain.from_iterable flattens nested lists into a single list
        # nested for loop can also be used
        return sum(1 for i in itertools.chain.from_iterable(self.board) if i == GameOfLife.ALIVE)

    def dead(self):
        # or len(self.board) * len(self.board[0]) - self.alive()
        return sum(1 if i == GameOfLife.DEAD else 0 for i in itertools.chain.from_iterable(self.board))

    def __repr__(self):
        repr = ""
        for row in self.board:
            """
            Strings are immutable, so `str += x` copies str and adds `x`.
            In Python3 there is an optimization that doesn't copy `str` if there is only one pointer to it.
            This is the case here.
            """
            repr += "{}\n".format("".join(row))
        return repr


def play_game(game, n):
    for i in range(n):
        print(game)
        game = game.move()
        time.sleep(0.5)  # sleep to see the output
