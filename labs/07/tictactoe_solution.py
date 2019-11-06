import sys
from contextlib import contextmanager

from PyQt5.QtCore import QPoint, pyqtSignal
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

from game_solution import CellState, Game
from minmax_player import ProcessPlayer


@contextmanager
def painter_ctx(painter):
    painter.save()
    yield
    painter.restore()


class GameBoard(QWidget):
    slotClicked = pyqtSignal(int, int)

    def __init__(self, width, dimension, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(width, width)
        self.dimension = dimension
        self.cell_width = int(width / dimension)

        self.game = None
        self.set_game(game)

    def set_game(self, game):
        self.game = game

    def paintEvent(self, *args, **kwargs):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(0, 0, self.width(), self.height(), QColor("white"))

        for y in range(self.dimension):
            for x in range(self.dimension):
                start_x = x * self.cell_width
                start_y = y * self.cell_width
                painter.drawRect(start_x,
                                 start_y,
                                 start_x + self.cell_width,
                                 start_y + self.cell_width)
                cell = self.game.get_cell_state(y, x)
                self.draw_cell(painter, start_x, start_y, cell)

    def draw_cell(self, painter, x, y, cell):
        if cell == CellState.Cross:
            with painter_ctx(painter):
                painter.fillRect(x, y, self.cell_width, self.cell_width, QColor("red"))
                painter.fillRect(x, y, self.cell_width, self.cell_width / 2, QColor("white"))
                painter.setBrush(QColor("blue"))
                painter.drawConvexPolygon(*[QPoint(x, y) for (x, y) in [
                    (x, y),  # top left
                    (x, y + self.cell_width),  # bottom left
                    (x + self.cell_width / 2, y + self.cell_width / 2)  # center
                ]])
        elif cell == CellState.Circle:
            with painter_ctx(painter):
                painter.setBrush(QColor("white"))
                painter.drawRect(x, y, self.cell_width, self.cell_width)
                painter.setBrush(QColor("red"))
                painter.drawEllipse(QPoint(x + self.cell_width / 2, y + self.cell_width / 2),
                                    self.cell_width / 4, self.cell_width / 4)

    def mousePressEvent(self, event):
        mouse_x = event.x()
        mouse_y = event.y()
        cell_x, cell_y = self.get_cell_location(mouse_x, mouse_y)

        if cell_x >= self.dimension or cell_y >= self.dimension:
            return

        self.slotClicked.emit(cell_y, cell_x)

    def get_cell_location(self, mouse_x, mouse_y):
        x = int(mouse_x / self.cell_width)
        y = int(mouse_y / self.cell_width)
        return (x, y)


class TicTacToe(QWidget):
    def __init__(self, dimension, width, length, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Piškvorky")

        self.dimension = dimension
        self.game = Game(dimension, length, active_player=1)
        self.length = length

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        button = QPushButton("Reset game")
        button.clicked.connect(self.reset)
        self.layout.addWidget(button)

        self.active_player_label = QLabel("Player 0")
        self.layout.addWidget(self.active_player_label)

        self.gameboard = GameBoard(width, dimension, self.game)
        self.gameboard.slotClicked.connect(self.handle_click)
        self.layout.addWidget(self.gameboard)

        self.player = ProcessPlayer()

        # self.play_minmax()
        self.draw_board()

    def handle_click(self, cell_y, cell_x):
        res = self.game.move(cell_y, cell_x)
        self.handle_move(res)

        # if not res[2]:
        #     self.play_minmax()
        # else:
        self.draw_board()

    def play_minmax(self):
        if self.game.active_player == 1:
            res = self.player.play(self.game, self.game.active_player)
            self.handle_move(res)
            self.draw_board()

    def handle_move(self, res):
        (valid, win, done) = res
        if not valid:
            print("Invalid move")
        if win is not None:
            self.end("Player {} has won!".format(win))
        elif done:
            self.end("Draw")

    def draw_board(self):
        self.active_player_label.setText("Player {}".format(self.game.active_player))
        self.gameboard.repaint()

    def reset(self):
        self.game = Game(self.dimension, self.length)
        self.gameboard.set_game(self.game)
        self.draw_board()

    def end(self, message):
        print(message)
        app.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tictactoe = TicTacToe(10, 400, 5)
    tictactoe.show()
    sys.exit(app.exec_())
