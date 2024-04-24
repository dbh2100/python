"""This module defines a Python representation of a Rubik's cube"""

from collections import deque

class _CubeFace:

    __slots__ = ['_squares', 'top', 'bottom', 'left', 'right', 'back']

    def __init__(self, size, color=None, colors=None, recursion=False):

        # Set each face square to initial color provided in constructor
        self._squares = squares = []
        color = color or colors[0]
        for _ in range(size):
            squares.append(size * [color])

        # Do not create other faces if constructor called recursively
        if recursion:
            return

        # Create other faces and set their connections
        self.top    = top    = _CubeFace(size, color=colors[1], recursion=True)
        self.bottom = bottom = _CubeFace(size, color=colors[2], recursion=True)
        self.left   = left   = _CubeFace(size, color=colors[3], recursion=True)
        self.right  = right  = _CubeFace(size, color=colors[4], recursion=True)
        back                 = _CubeFace(size, color=colors[5], recursion=True)

        top.top, top.bottom, top.left, top.right             = left, right, self, back
        bottom.top, bottom.bottom, bottom.left, bottom.right = right, left, back, self
        left.top, left.bottom, left.left, left.right         = self, back, top, bottom
        right.top, right.bottom, right.left, right.right     = back, self, bottom, top
        back.top, back.bottom, back.left, back.right         = bottom, top, right, left

    def __repr__(self):
        border = '\n _ _ _ \n'
        rows = ['|' + '|'.join(self[i]) + '|' for i in range(3)]
        return border + border.join(rows) + border

    def __getitem__(self, index):
        return self._squares.__getitem__(index)

    def __setitem__(self, index, value):
        self._squares.__setitem__(index, value)

    @property
    def inner_edge(self):
        """The face's outer squares"""
        top_edge = [self[0][0], self[0][1]]
        right_edge = [self[0][2], self[1][2]]
        bottom_edge = [self[2][2], self[2][1]]
        left_edge = [self[2][0], self[1][0]]
        return top_edge + right_edge + bottom_edge + left_edge

    @inner_edge.setter
    def inner_edge(self, values):
        self[0][0] = values[0]
        self[0][1] = values[1]
        self[0][2] = values[2]
        self[1][2] = values[3]
        self[2][2] = values[4]
        self[2][1] = values[5]
        self[2][0] = values[6]
        self[1][0] = values[7]

    @property
    def outer_edge(self):
        """The adjacent faces' squares bordering this face"""
        top, bottom, left, right = self.top, self.bottom, self.left, self.right
        top_edge = [top[0][0], top[1][0], top[2][0]]
        right_edge = [right[2][2], right[2][1], right[2][0]]
        bottom_edge = [bottom[2][2], bottom[1][2], bottom[0][2]]
        left_edge = [left[0][0], left[0][1], left[0][2]]
        return top_edge + right_edge + bottom_edge + left_edge

    @outer_edge.setter
    def outer_edge(self, values):

        top, bottom, left, right = self.top, self.bottom, self.left, self.right

        top[0][0] = values[0]
        top[1][0] = values[1]
        top[2][0] = values[2]

        right[2][2] = values[3]
        right[2][1] = values[4]
        right[2][0] = values[5]

        bottom[2][2] = values[6]
        bottom[1][2] = values[7]
        bottom[0][2] = values[8]

        left[0][0] = values[9]
        left[0][1] = values[10]
        left[0][2] = values[11]

    def rotate(self, direction):
        """Rotate face

        direction is either 'left' or 'right'
        """

        inner_edge_colors = deque(self.inner_edge)
        outer_edge_colors = deque(self.outer_edge)

        if direction.lower() == 'left':
            inner_edge_colors.rotate(-2)
            outer_edge_colors.rotate(-3)
        elif direction.lower() == 'right':
            inner_edge_colors.rotate(2)
            outer_edge_colors.rotate(3)
        else:
            raise ValueError('direction must be "left" or "right"')

        self.inner_edge = inner_edge_colors
        self.outer_edge = outer_edge_colors

    def all_same_color(self):
        """Check if all the face's squares are the same color"""
        return len(set(self[0] + self[1] + self[2])) == 1

    def reset_color(self):
        """Switch the squares' color to that of the center square"""
        squares = self._squares
        n = len(squares)
        m = n // 2
        color = squares[m][m]
        for row in squares:
            for i in range(n):
                row[i] = color


class RubiksCube:
    """Python class representing a Rubik's cube"""

    COLORS = ['red', 'blue', 'green', 'yellow', 'white', 'orange']

    __slots__ = ['_size', '_faces'] + COLORS

    def __init__(self, size=3) -> None:

        colors = [color[0].upper() for color in self.COLORS]

        faces = self._faces = 6 * [None]
        self.red = faces[0] = face0 = _CubeFace(size, colors=colors)
        self.blue = faces[1] = face0.top
        self.green = faces[2] = face0.bottom
        self.yellow = faces[3] = face0.left
        self.white = faces[4] = face0.right
        self.orange = faces[5] = face0.top.right

    def __repr__(self):
        return '\n'.join(str(face) for face in self._faces)

    def is_solved(self):
        """Determine if all squares on each face have same color"""
        return all(face.all_same_color() for face in self._faces)

    def reset(self):
        """Revert all the squares back to their original color"""
        for face in self._faces:
            face.reset_color()


if __name__ == '__main__':

    cube = RubiksCube()
    print('Cube is initally solved:', cube.is_solved())

    # Rotate the red face to the left
    cube.red.rotate('left')
    print('Cube after left rotation:')
    print(cube)
    print('Cube is solved after left rotation:', cube.is_solved())

    print(50 * '*')

    # Rotate the red face to the right
    cube.red.rotate('right')
    print('Cube after right rotation:')
    print(cube)
    print('Cube is solved after right rotation:', cube.is_solved())

    print(50 * '*')

    # Scramble the cube to test reset
    cube.blue.rotate('right')
    cube.white.rotate('left')
    cube.yellow.rotate('left')
    print('Cube after scramble')
    print(cube)
    print('Cube is solved after scramble:', cube.is_solved())

    print(50 * '*')

    # Reset the cube
    cube.reset()
    print('Cube after reset')
    print(cube)
    print('Cube is solved after reset:', cube.is_solved())
