"""Design Connect4 Game"""

class Connect4:
    """Connect4 game class"""

    __slots__ = ('_num_rows', '_num_cols', '_circles', '_current_player')

    def __init__(self, num_rows, num_cols) -> None:
        """num_rows and num_cols must be intergers of at least 4"""

        if not isinstance(num_rows, int) or not isinstance(num_cols, int):
            raise TypeError('Number of rows and columns must both be integers')
        if num_rows < 4 or num_cols < 4:
            raise ValueError('Number of rows and columns must both be at least 4')
        self._num_rows = num_rows
        self._num_cols = num_cols

        circles = []
        for _ in range(self._num_rows):
            circles.append(self._num_cols * [''])
        self._circles = circles
        self._current_player = 'Red'

    def check_row(self, i0: int, j0: int, color: str) -> bool:
        """i0, j0, and color are the row, column, and color of the newly-placed circle
        Return boolean indicating whether the move ends the game
        """
        j_start = max(j0 - 3, 0)
        j_end = min(j0 + 4, self._num_cols)
        circles = self._circles
        count = 0
        for j in range(j_start, j_end):
            if circles[i0][j] == color:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False

    def check_column(self, i0: int, j0: int, color: str) -> bool:
        """i0, j0, and color are the row, column, and color of the newly-placed circle
        Return boolean indicating whether the move ends the game
        """
        i_start = max(i0 - 3, 0)
        i_end = min(i0 + 4, self._num_rows)
        circles = self._circles
        count = 0
        for i in range(i_start, i_end):
            if circles[i][j0] == color:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False

    def check_diagonals(self, i0: int, j0: int, color: str) -> bool:
        """i0, j0, and color are the row, column, and color of the newly-placed circle
        Return boolean indicating whether the move ends the game
        """
        circles = self._circles
        m = self._num_rows
        n = self._num_cols
        for diag in (-1, 1):
            count = 0
            for di in range(-3, 4):
                i = i0 + di
                j = j0 + diag * di
                if not 0 <= i < m or not 0 <= j < n:
                    continue
                if circles[i][j] == color:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
        return False

    def is_game_over(self, i0: int, j0: int, color: str) -> bool:
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

            for factor in range(-3, 4):

                i = i0 + (factor * di)
                j = j0 + (factor * dj)

                if not 0 <= i < m or not 0 <= j < n:
                    continue

                if circles[i][j] == color:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0

        return False

    def place_circle(self, j: int, color: str) -> bool:
        """Returns boolean indicating whether move ends game"""

        i = 0
        m = self._num_rows
        circles = self._circles
        while i + 1 < m and not circles[i+1][j]:
            i += 1
        circles[i][j] = color

        # Check if game is over
        return self.is_game_over(i, j ,color)

    def enter_move(self) -> bool:
        """Prompt the player to pick where to place circle"""

        j = -1
        n = self._num_cols
        player = self._current_player
        circles = self._circles

        msg = f'{player}, enter column to place circle(1 - {n}): '
        while not 0 <= j < n:
            j_str = input(msg)
            try:
                j = int(j_str) - 1
            except ValueError:
                continue
            if not 0 <= j < n:
                print('Invalid column')
                continue
            # If all chosen column's circles are filled,
            # user needs to choose diferent column
            if circles[0][j]:
                print('You must choose a different column')
                j = -1

        # Place circle and determine if move ends game
        # If so, display board one last time and print message
        if self.place_circle(j, player):
            self.display_board()
            print(f'{player} wins!')
            return True

        # Check if circle can no longer be placed
        if all(circles[0][j] for j in range(self._num_cols)):
            print('Game is a draw')
            return True

        # Switch player
        self._current_player = 'Black' if player == 'Red' else 'Red'

        return False

    def display_board(self) -> None:
        """Display the Connect4 board"""

        n = self._num_cols

        # Print 1-indexed column numbers
        print(' '.join([str(j+1).center(5) for j in range(n)]))

        # Print circle values
        circles = self._circles
        for i in range(self._num_rows):
            print('|'.join([circles[i][j].center(5) for j in range(n)]))
            print(' '.join([5 * '_' for _ in range(n)]))

    def play_game(self) -> None:
        """Start the game"""
        game_over = False
        while not game_over:
            self.display_board()
            game_over = self.enter_move()


if __name__ == '__main__':
    Connect4(5, 6).play_game()
