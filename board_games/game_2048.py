"""Defines a Python version of the popular mobile game 2048"""

from random import random, randint
from array import array
from functools import partial

class Game2048:
    """Class simulating the popular mobile game 2048"""

    # Can be overriden in a subclass
    TARGET_VALUE = 2048

    __slots__ = ('_size', '_squares', '_max_value', '_num_blanks')

    def __init__(self, size=3):
        self._size = size
        self._squares = []
        for _ in range(size):
            #'H' is unsigned short
            self._squares.append(array('H', size*[0]))
        self._max_value = 0
        self._num_blanks = size * size

    def _place_value(self):
        """Place either 2 or 4 on a random empty square"""

        size = self._size
        squares = self._squares
        gen_index = partial(randint, 0, size-1)

        i, j = gen_index(), gen_index()
        while squares[i][j]:
            i, j = gen_index(), gen_index()

        squares[i][j] = 2 if random() < 0.5 else 4

        self._max_value = max(squares[i][j], self._max_value)
        self._num_blanks -= 1

    def _move_value(self, i1, j1, i2, j2):
        """Move square value from i1, j1 to i2, j2
        and return value in destination square
        """

        squares = self._squares

        if not squares[i1][j1]:
            return

        if not squares[i2][j2]:
            squares[i1][j1], squares[i2][j2] = 0, squares[i1][j1]

        if squares[i1][j1] == squares[i2][j2]:
            squares[i1][j1], squares[i2][j2] = 0, 2 * squares[i1][j1]
            self._num_blanks += 1
            self._max_value = max(squares[i2][j2], self._max_value)

    def _get_move(self):
        """Get and execute player's input, returning maximum value on board"""

        moves = {'up', 'left', 'right', 'down'}
        direction = None
        while direction not in moves:
            direction = input('Enter move (up, down, left, or right): ').lower()

        size = self._size
        srange = range(size)

        if direction == 'up':
            for i in reversed(range(1, size)):
                for j in srange:
                    self._move_value(i, j, i-1, j)

        if direction == 'left':
            for j in reversed(range(1, size)):
                for i in srange:
                    self._move_value(i, j, i, j-1)

        if direction == 'right':
            for j in range(size-1):
                for i in srange:
                    self._move_value(i, j, i, j+1)

        if direction == 'down':
            for i in range(size - 1):
                for j in srange:
                    self._move_value(i, j, i+1, j)

    def _can_move(self):
        """Returns True if another move can be made, False otherwise"""

        # Player can make a move if any square is empty
        if self._num_blanks:
            return True

        squares = self._squares

        for i in range(self._size - 1):

            for j in range(self._size - 1):

                # Check if square has same value as one to its right
                if squares[i][j] == squares[i][j+1]:
                    return True

                # Check if square has same value as one below it
                if squares[i][j] == squares[i+1][j]:
                    return True

        return False

    def display(self):
        """Display the board"""

        row_boundary = ' '.join(self._size * ['____'])

        # Print top of board
        print(row_boundary)

        for row in self._squares:

            row_display = []
            for square in row:
                square_display = str(square).center(4) if square else '    '
                row_display.append(square_display)

            # Print row and row boundary
            print('|' + '|'.join(row_display) + '|')
            print(row_boundary)

    def clear(self):
        """Clear the board"""
        srange = range(self._size)
        for row in self._squares:
            for i in srange:
                row[i] = 0

    def play(self):
        """Start the game"""

        # Start by clearing the board
        self.clear()

        while self._max_value < self.TARGET_VALUE:

            # If there is an empty square, place 2 or 4 there
            if self._num_blanks:
                self._place_value()

            self.display()

            # Exit game if no move can be made
            if not self._num_blanks and not self._can_move():
                print('Game over: no more moves')

            # Get the user's move
            self._get_move()

        # When user gets 2048 square,
        # display the board one last time and the message
        self.display()
        print(f'You got the {self.TARGET_VALUE} square!')


if __name__ == '__main__':
    Game2048().play()
