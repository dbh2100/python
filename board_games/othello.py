DIRECTIONS = [
    (-1, -1), # up and left
    (-1, 0),  # up
    (-1, 1),  # up and right
    (0, -1),  # left
    (0, 1),   # right
    (1, -1),  # down and left
    (1, 0),   # down
    (1, 1),   # down and right
]

BLANK_SPACE = '*****'

PLAYERS = ['Black', 'White']


class Othello:

    __slots__ = ('_num_rows', '_num_cols', '_squares', '_num_squares',
                 '_current_player', '_scores')

    def __init__(self, num_rows, num_cols):
        self._num_rows = num_rows
        self._num_cols = num_cols
        squares = list()
        for _ in range(num_rows):
            squares.append(num_cols * [BLANK_SPACE])
        self._squares = squares
        self._current_player = PLAYERS[0]
        self._scores = [0, 0]
        self._num_squares = num_rows * num_cols

    def _is_in_bounds(self, i, j):
        """Determine if (i, j) is in the board's boundaries"""
        return 0 <= i < self._num_rows and 0 <= j < self._num_cols

    def place_stone(self, i0, j0, color):
        """i0 and j0 are the coordinates where the stone is placed

        color is the color of the stone to be placed
        """

        squares = self._squares
        player_index = PLAYERS.index(color)
        other_color = PLAYERS[1-player_index]

        # Place stone in square and increment player's score
        squares[i0][j0] = color
        self._scores[player_index] += 1

        for di, dj in DIRECTIONS:

            squares_in_range = list()

            i, j = i0 + di, j0 + dj

            while self._is_in_bounds(i, j) and squares[i][j] == other_color:
                squares_in_range.append((i, j))
                count += 1
                i += di
                j += dj

            # Flip stones if sandwiched by player's color
            i1, j1 = i, j
            if self._is_in_bounds(i1, j1) and squares[i1][j1] == color:
                for i, j in squares_in_range:
                    squares[i][j] = color
                    self._scores[player_index] += 1
                    self._scores[1-player_index] -= 1

    def enter_move(self):
        """Get square stone is placed based on current player's input"""

        i, j = -1, -1
        while not self._is_in_bounds(i, j) or self._squares[i][j] != BLANK_SPACE:
            spot = input('%s, place stone (row, column): ' % self._current_player)
            try:
                i, j = map(int, spot.split(','))
            except ValueError:
                continue

        self.place_stone(i, j, self._current_player)

        if self._current_player == PLAYERS[0]:
            self._current_player = PLAYERS[1]
        else:
            self._current_player = PLAYERS[0]

    def evaluate_board(self):
        """Determine if game is over based on sum of scores

        If the game is over, output winnner
        """

        if self._scores[0] + self._scores[1] < self._num_squares:
            return False

        # Display board one last time
        self.display_board()

        # Announce result
        if self._scores[0] > self._scores[1]:
            print('%s wins!' % PLAYERS[0])
        elif self._scores[0] < self._scores[1]:
            print('%s wins!' % PLAYERS[1])
        else:
            print('Tie game')
        return True

    def display_board(self):

        n = self._num_cols

        # Print 0-indexed column numbers
        print(' '.join([str(j).center(5) for j in range(n)]))

        # Print row numbers and square values
        squares = self._squares
        for i in range(self._num_rows):
            print(str(i) + ' ' + '|'.join([squares[i][j] for j in range(n)]))
            print('  ' + ' '.join([5 * '_' for j in range(n)]))

        # Display scores
        print('%s: %d; %s: %d' %
              (PLAYERS[0], self._scores[0], PLAYERS[1], self._scores[1]))

    def play_game(self):
        game_over = False
        while not game_over:
            self.display_board()
            self.enter_move()
            game_over = self.evaluate_board()


if __name__ == '__main__':
    Othello(6, 5).play_game()
