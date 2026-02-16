'''Defining a game of chess'''

from __future__ import annotations
from typing import Optional
from string import ascii_lowercase
from abc import ABC, abstractmethod
from enum import Enum, auto


def alphanumeric_to_coordinates(alphanumeric: str) -> tuple[Optional[int], Optional[int]]:
    ''' Convert alphanumeric to integer coordinates

    alphanumeric_to_coordinates('B4') = (1, 3)
    '''
    try:
        letter, number = alphanumeric
        x = ascii_lowercase.index(letter.lower())
        y = int(number) - 1
    except ValueError:
        return (None, None)
    else:
        return (x, y)


class Color(Enum):
    WHITE = auto()
    BLACK = auto()


class Piece(ABC):
    '''Abstract base class for chess pieces'''

    def __init__(self, board: Board, color: Color, initial_x: int, initial_y: int) -> None:
        self._board = board
        self._color = color
        self._x = initial_x
        self._y = initial_y
        self._captured = False

    def __repr__(self) -> str:
        return self.color.name[0] + self.__class__.__name__[0]

    @property
    def color(self):
        '''The piece's color'''
        return self._color

    @property
    def x(self):
        '''The column index'''
        return self._x

    @property
    def y(self):
        '''The row index'''
        return self._y

    @abstractmethod
    def _is_valid_move(self, x, y) -> bool:
        raise NotImplementedError

    def _valid_moves(self) -> list[tuple[int, int]]:
        range8 = range(8)
        return [(i, j) for i in range8 for j in range8 if self._is_valid_move(i, j)]

    def move(self, x: int, y: int) -> bool:
        '''Move the piece, return True if valid move, False otherwise'''

        if (x, y) not in self._valid_moves():
            return False

        if (other_piece := self._board.squares[y][x]) is not None:
            if other_piece.color != self.color:
                other_piece.capture()
                if isinstance(other_piece, King):
                    self._board.winner = self.color
            else:
                return False

        self._x = x
        self._y = y

        return True
 
    def capture(self):
        self._captured = True


class Pawn(Piece):
    '''The pawn piece'''

    def __init__(self, board: Board, color: Color, initial_x: int, initial_y: int) -> None:
        super().__init__(board, color, initial_x, initial_y)
        self._has_moved = False

    def _is_valid_move(self, x, y) -> bool:

        if not (0 <= x < 8 and 0 <= y < 8):
            return False

        if (other_piece := self._board.squares[y][x]) is not None:
            if other_piece.color == self.color:
                return False

        step = 1 if self.color == list(Color)[0] else -1

        if not self._has_moved:
            if x == self._x and y == self._y + step*2:
                return True

        if x == self._x and y == self._y + step:
            return True

        # Capturing diagonally
        if x in (self._x+1, self._x-1) and y == self._y + step:
            if (other_piece := self._board.squares[y][x]) is not None:
                if other_piece.color != self.color:
                    return True

        return False

    def move(self, x: int, y: int) -> bool:
        is_moving = super().move(x, y)
        if is_moving:
            self._has_moved = True
        return is_moving


class Rook(Piece):
    '''The rook piece'''

    def _is_valid_move(self, x, y) -> bool:

        if not (0 <= x < 8 and 0 <= y < 8):
            return False

        if x != self._x and y != self._y:
            return False

        # Check if there are pieces in the way
        if x == self._x:
            step = 1 if y > self._y else -1
            for i in range(self._y + step, y+step, step):
                if (other_piece := self._board.squares[i][x]) is not None:
                    if i != y or other_piece.color == self.color:
                        return False
        else:  # y == self._y
            step = 1 if x > self._x else -1
            for i in range(self._x + step, x+step, step):
                if (other_piece := self._board.squares[y][i]) is not None:
                    if i != x or other_piece.color == self.color:
                        return False

        return True


class Knight(Piece):
    '''The knight piece'''

    def _is_valid_move(self, x, y) -> bool:

        if not (0 <= x < 8 and 0 <= y < 8):
            return False

        if (other_piece := self._board.squares[x][y]) is not None:
            if other_piece.color == self.color:
                return False

        dx = abs(x - self._x)
        dy = abs(y - self._y)

        return (dx, dy) in [(1, 2), (2, 1)]


class Bishop(Piece):
    '''The bishop piece'''

    def _is_valid_move(self, x, y) -> bool:

        if not (0 <= x < 8 and 0 <= y < 8):
            return False

        if abs(x - self._x) != abs(y - self._y):
            return False

        # Check if there are pieces in the way
        step_x = 1 if x > self._x else -1
        step_y = 1 if y > self._y else -1
        for i in range(1, abs(x - self._x)):
            if (other_piece := self._board.squares[self._x + i*step_x][self._y + i*step_y]) is not None:
                if other_piece.color == self.color:
                    return False

        return True


class Queen(Bishop, Rook):
    '''The queen piece'''

    def _is_valid_move(self, x, y) -> bool:
        if x == self._x or y == self._y:
            # Rook-like movement
            return Rook._is_valid_move(self, x, y)
        elif abs(x - self._x) == abs(y - self._y):
            # Bishop-like movement
            return Bishop._is_valid_move(self, x, y)
        return False


class King(Piece):
    '''The king piece'''

    def _is_valid_move(self, x, y) -> bool:

        if not (0 <= x < 8 and 0 <= y < 8):
            return False

        if (other_piece := self._board.squares[x][y]) is not None:
            if other_piece.color == self.color:
                return False

        dx = abs(x - self._x)
        dy = abs(y - self._y)

        return max(dx, dy) == 1


class Board:
    '''Chess board'''

    def __init__(self) -> None:

        row1 = [
            Rook(self, Color.WHITE, 0, 0),
            Knight(self, Color.WHITE, 1, 0),
            Bishop(self, Color.WHITE, 2, 0),
            Queen(self, Color.WHITE, 3, 0),
            King(self, Color.WHITE, 4, 0),
            Bishop(self, Color.WHITE, 5, 0),
            Knight(self, Color.WHITE, 6, 0),
            Rook(self, Color.WHITE, 7, 0),
        ]
        row2 = [Pawn(self, Color.WHITE, i, 1) for i in range(8)]

        row7 = [Pawn(self, Color.BLACK, i, 6) for i in range(8)]
        row8 = [
            Rook(self, Color.BLACK, 0, 7),
            Knight(self, Color.BLACK, 1, 7),
            Bishop(self, Color.BLACK, 2, 7),
            Queen(self, Color.BLACK, 3, 7),
            King(self, Color.BLACK, 4, 7),
            Bishop(self, Color.BLACK, 5, 7),
            Knight(self, Color.BLACK, 6, 7),
            Rook(self, Color.BLACK, 7, 7),
        ]

        self.squares = [
            row1,
            row2,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            row7,
            row8,
        ]

        self._current_turn = Color.WHITE

        self.winner: Optional[Color] = None

    def display_board(self) -> None:
        '''Display the board'''
        range8 = range(8)
        print('  A    B    C    D    E    F    G    H')
        print('  ' +' '.join([4 * '_' for _ in range8]))
        for i, row in enumerate(self.squares):
            print(f'{i+1}' + ' '.join(repr(piece).center(4) if piece else '    ' for piece in row))
            print('  ' + ' '.join([4 * '_' for _ in range8]))

    def get_move(self) -> bool:
        '''Enter move like "B2 to B4"

        Return True if game is over
        '''

        player_input = input(f'Enter move {self._current_turn.name}: ')
        start, destination = '', ''
        try:
            start, destination = player_input.split(' to ')
        except ValueError:
            print(f'Invalid move: {player_input}')
            return False

        # Find piece at starting location
        start_x, start_y = alphanumeric_to_coordinates(start)
        if start_y is None:
            print(f'Invalid starting coordinates: {start}')
            return False
        piece = self.squares[start_y][start_x]
        if piece is None:
            print(f'Invalid move: no piece found on {start}')
            return False
        if piece.color != self._current_turn:
            print(f'Invalid move: it is {self._current_turn.name}\'s turn')
            return False

        # Move piece if possible
        dest_x, dest_y = alphanumeric_to_coordinates(destination)
        if dest_y is None:
            print(f'Invalid destination coordinates: {destination}')
            return False
        if not piece.move(dest_x, dest_y):
            print(f'Cannot move piece at {start} to {destination}')
            return False
        self.squares[dest_y][dest_x] = piece
        self.squares[start_y][start_x] = None

        # Check if game is over
        if self.winner is not None:
            return True

        # Switch player if move was valid
        if self._current_turn == Color.WHITE:
            self._current_turn = Color.BLACK
        else:
            self._current_turn = Color.WHITE

        return False

    def play(self):
        game_over = False
        while not game_over:
            self.display_board()
            game_over = self.get_move()
        self.display_board()
        if self.winner is not None:
            print(f'{self.winner.name} wins!')


if __name__ == '__main__':
    Board().play()
