from enum import Enum


class CellState(Enum):
    Empty = 0
    Cross = 1
    Circle = 2


def invalid_move():
    return (False, None, False)


def valid_move(win, done):
    return (True, win, done)


class Game(object):
    def __init__(self, dimension, length, active_player=0):
        self.dimension = dimension
        self.length = length

        self.board = [CellState.Empty for _ in range(dimension**2)]
        self.active_player = active_player
        self.last_move = None

    def get_cell_state(self, row, col):
        return self.board[self.get_index(row, col)]

    def move(self, row, col, check_win=True):
        if not self.is_valid(row, col):
            return invalid_move()

        cell = self.get_cell_state(row, col)
        if cell is not CellState.Empty:
            return invalid_move()

        player_cell = self.get_player_cell(self.active_player)
        self.board[self.get_index(row, col)] = player_cell
        if check_win:
            (winner, done) = self.get_state(self.active_player)
        else:
            (winner, done) = (None, False)

        self.swap_players()

        self.last_move = row * self.dimension + col
        return valid_move(winner, done)

    def get_state(self, player):
        winner = None
        if self.check_win(player):
            winner = player
        done = not any([cell == CellState.Empty for cell in self.board])
        return (winner, done or winner is not None)

    def copy(self):
        game = Game(self.dimension, self.length)
        game.board = self.board[:]
        game.active_player = self.active_player
        return game

    def get_index(self, row, col):
        return row * self.dimension + col

    def get_player_cell(self, player):
        return CellState.Cross if player == 0 else CellState.Circle

    def swap_players(self):
        self.active_player = 1 - self.active_player

    def check_win(self, player, length=None):
        if length is None:
            length = self.length

        cell = self.get_player_cell(player)
        increments = ((1, 0), (0, 1), (1, 1), (-1, 1))

        for y in range(self.dimension):
            for x in range(self.dimension):
                for increment in increments:
                    pos_x = x
                    pos_y = y
                    counter = 0
                    while (self.is_valid(pos_x, pos_y) and
                           self.get_cell_state(pos_y, pos_x) == cell):
                        counter += 1
                        pos_x += increment[0]
                        pos_y += increment[1]
                    if counter >= length:
                        return True
        return False

    def is_valid(self, x, y):
        return 0 <= x < self.dimension and 0 <= y < self.dimension

    def hash(self):
        return (tuple(self.board), self.active_player)

    def __str__(self):
        buf = ""
        chars = {
            CellState.Empty: '_',
            CellState.Cross: 'x',
            CellState.Circle: 'o'
        }

        for y in range(self.dimension):
            for x in range(self.dimension):
                cell = self.get_cell_state(y, x)
                buf += chars[cell]
            buf += "\n"
        return buf
