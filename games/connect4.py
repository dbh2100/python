"""Design Connect4 Game"""

from enum import Enum, auto

class _Player(Enum):
    """Represents each player and the color of their pieces"""
    RED = 0
    BLACK = 1


class _Circle(Enum):
    """Represents each circle in the game board"""
    BLANK = auto()
    RED = auto()
    BLACK = auto()

_CircleGrid = list[list[_Circle]]


class Connect4:
    """Connect4 game class"""

    __slots__ = ('_num_rows', '_num_cols', '_circles', '_current_player')

    def __init__(self, num_rows: int, num_cols: int) -> None:
        """num_rows and num_cols must be intergers of at least 4"""

        if not isinstance(num_rows, int) or not isinstance(num_cols, int):
            raise TypeError('Number of rows and columns must both be integers')
        if num_rows < 4 or num_cols < 4:
            raise ValueError('Number of rows and columns must both be at least 4')
        self._num_rows = num_rows
        self._num_cols = num_cols

        circles: _CircleGrid = []
        for _ in range(self._num_rows):
            circles.append(self._num_cols * [_Circle.BLANK])
        self._circles = circles
        self._current_player = _Player.RED

    def _is_game_over(self, i0: int, j0: int, color: str) -> bool:
        """i0, j0, and color are the row, column, and color of the newly-placed circle
        Return boolean indicating whether the move ends the game
        """

        circles = self._circles
        m = self._num_rows
        n = self._num_cols

        for di, dj in [
            (0, 1), # row
            (1, 0), # column
            (1, 1), # upper-left to lower-right diagonal
            (-1, 1), # upper-right to lower-left diagonal
        ]:

            count = 0

            for offset in range(-3, 4):

                i = i0 + (offset * di)
                j = j0 + (offset * dj)

                if not 0 <= i < m or not 0 <= j < n:
                    continue

                if circles[i][j].name == color:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0

        return False

    def _place_circle(self, j: int, color: str) -> bool:
        """Returns boolean indicating whether move ends game"""

        i: int = 0
        m = self._num_rows
        circles = self._circles
        print(circles[i+1][j].name)
        while i + 1 < m and circles[i+1][j] == _Circle.BLANK:
            i += 1
        circles[i][j] = _Circle[color]

        # Check if game is over
        return self._is_game_over(i, j, color)

    def enter_move(self) -> bool:
        """Prompt the player to pick where to place circle"""

        j: int = -1
        n = self._num_cols
        player = self._current_player
        circles = self._circles

        msg: str = f'{player.name}, enter column to place circle(1 - {n}): '
        while not 0 <= j < n:
            j_str: str = input(msg)
            try:
                j = int(j_str) - 1
            except ValueError:
                print(f'{j_str} is not a valid column number')
                continue
            if not 0 <= j < n:
                print(f'{j_str} is not a valid column number')
                continue
            # If all chosen column's circles are filled,
            # user needs to choose diferent column
            if circles[0][j] != _Circle.BLANK:
                print('You must choose a different column')
                j = -1

        # Place circle and determine if move ends game
        # If so, display board one last time and print message
        if self._place_circle(j, player.name):
            self.display_board()
            print(f'{player.name} wins!')
            return True

        # Check if circle can no longer be placed
        if all(circles[0][j] != _Circle.BLANK for j in range(self._num_cols)):
            print('Game is a draw')
            return True

        # Switch player
        self._current_player = _Player(1 - player.value)

        return False

    def display_board(self) -> None:
        """Display the Connect4 board"""

        n = self._num_cols
        columns = range(self._num_cols)

        # Print 1-indexed column numbers
        print(' '.join([str(j+1).center(5) for j in range(n)]))

        # Print circle values
        circles = self._circles
        for i in range(self._num_rows):
            circle_display = []
            for j in columns:
                circle = circles[i][j]
                if circle == _Circle.BLANK:
                    circle_display.append(5*' ')
                else:
                    circle_display.append(circle.name.center(5))
            print('|'.join(circle_display))
            print(' '.join([5 * '_' for _ in range(n)]))

    def play_game(self) -> None:
        """Start the game"""
        game_over = False
        while not game_over:
            self.display_board()
            game_over = self.enter_move()


if __name__ == '__main__':
    Connect4(5, 6).play_game()
