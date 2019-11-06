import multiprocessing
import time

from game_solution import CellState


class ProcessPlayer:
    def __init__(self):
        self.pool = multiprocessing.Pool()
        self.minmax = MinMaxPlayer()

    def play(self, game, player):
        empty = all(cell == CellState.Empty for cell in game.board)
        if empty:
            return game.move(game.dimension // 2, game.dimension // 2)

        alpha = -10e10
        beta = 10e10
        limit_max_depth = 5

        start = time.time()
        best_move = 0

        for i in range(1, limit_max_depth + 1):
            if time.time() - start > 5:  # search for max. 5 seconds
                print("Timeout")
                break
            print("Searching level {}...".format(i))

            moves = []
            args = []
            for move in self.minmax.gen_moves(game):
                g = game.copy()
                g.move(*self.minmax.get_pos(game, move), check_win=False)
                args.append((g, False, player, alpha, beta, i, 0))
                moves.append(move)

            values = list(self.pool.map(self.minmax.eval_game, args))
            if not values:
                return (False, None, True)

            best_move = moves[max(range(len(moves)), key=lambda index: values[index][1])]
        return game.move(*self.minmax.get_pos(game, best_move))


class MinMaxPlayer:
    """
    https://en.wikipedia.org/wiki/Minimax
    """
    def __init__(self):
        self.cache = {}

    def eval_game(self, args):
        game, maximizing, player, alpha, beta, max_depth, depth = args

        (winner, done) = game.get_state(1 - player if maximizing else player)
        if done or depth >= max_depth:
            value = self.get_score(game, winner, done, player, depth)
            if done:
                self.set_value(game, value)
            return (done, value)

        val = self.get_value(game)
        if val is not None:
            return (True, val)

        value = 10e10 * (-1 if maximizing else 1)
        done = False

        for move in self.gen_moves(game):
            g = game.copy()
            g.move(*self.get_pos(game, move), check_win=False)
            sub_done, next_val = self.eval_game((g, not maximizing, player, alpha, beta,
                                                 max_depth, depth + 1))
            if maximizing:
                value = max(value, next_val)
            else:
                value = min(value, next_val)

            if value == next_val:
                done = sub_done

            if maximizing:
                alpha = max(alpha, value)
            else:
                beta = min(beta, value)

            if alpha >= beta:
                break

        if done:
            self.set_value(game, value)
        return (done, value)

    def gen_moves(self, game, limit=16):
        vec = [0, 1]
        pos = self.get_pos(game, game.last_move)

        def turn():
            a, b = vec
            vec[0] = b
            vec[1] = -a

        move_left = 2
        length = 1
        active_length = length
        moves = []
        count = 0
        while True:
            pos = (pos[0] + vec[0], pos[1] + vec[1])
            if pos[0] < 0 or pos[1] < 0:
                break
            if game.is_valid(*pos):
                count += 1
                if game.get_cell_state(*pos) == CellState.Empty:
                    move = pos[0] * game.dimension + pos[1]
                    moves.append(move)
            active_length -= 1
            if active_length == 0:
                turn()
                move_left -= 1
                if move_left == 0:
                    move_left = 2
                    length = length + 1
                active_length = length

        for i in range(game.dimension ** 2):
            if game.get_cell_state(*self.get_pos(game, i)) == CellState.Empty and i not in moves:
                moves.append(i)
        """moves = []
        pos = self.get_pos(game, game.last_move or 0)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j and i == 0:
                    continue
                move = (pos[0] + i, pos[1] + j)
                if game.is_valid(*move) and game.get_cell_state(*move) == CellState.Empty:
                    moves.append(move[0] * game.dimension + move[1])

        for i in range(game.dimension ** 2):
            if i not in moves:
                moves.append(i)"""

        return moves[:limit]

    def get_pos(self, game, index):
        row = index // game.dimension
        col = index % game.dimension
        return (row, col)

    def get_score(self, game, winner, done, player, depth):
        if not done:
            """if depth > 4:
                for p in range(2):
                    chain = game.length - 1
                    if game.check_win(p, chain):
                        if p == player:
                            return 20 * chain - depth
                        return -(20 * chain - depth)"""
            return 0
        if done and winner is None:
            return 0
        if winner == player:
            return 20 * game.length - depth
        return -(20 * game.length - depth)

    def get_value(self, game):
        return self.cache.get(game.hash())

    def set_value(self, game, value):
        self.cache[game.hash()] = value
        return value
