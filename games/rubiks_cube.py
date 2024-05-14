"""This module defines a size-agnostic Python representation of a Rubik's cube"""

from collections import deque

class _CubeFace:

    __slots__ = [
        '_size', '_initial_color', '_squares',
        'top', 'bottom', 'left', 'right', 'back',
    ]

    def __init__(self, size, color=None, colors=None, recursion=False):

        self._size = size

        # Set each face square to initial color provided in constructor
        self._squares = squares = []
        color = self._initial_color = color or colors[0]
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
        rows = ['|' + '|'.join(self[i]) + '|' for i in range(self._size)]
        return border + border.join(rows) + border

    def __getitem__(self, index):
        return self._squares.__getitem__(index)

    def __setitem__(self, index, value):
        self._squares.__setitem__(index, value)

    @property
    def inner_edge(self):
        """The face's outer squares"""

        last = self._size - 1

        top_edge = self[0][:last]
        right_edge = [self[i][last] for i in range(last)]
        bottom_edge = self[last][last:0:-1]
        left_edge = [self[i][0] for i in range(last, 0, -1)]

        return top_edge + right_edge + bottom_edge + left_edge

    @inner_edge.setter
    def inner_edge(self, values):

        last = self._size - 1

        # Set top
        for i in range(last):
            self[0][i] = values[i]

        # Set right
        for i in range(last):
            self[i][last] = values[last+i]

        # Set bottom
        for i in range(1, self._size):
            self[last][i] = values[3*last-i]

        # Set left
        for i in range(1, self._size):
            self[0][last] = values[4*last-i]

    def _get_outer_edge(self, depth):
        """Get outer edge squares up to depth"""

        top, bottom, left, right = self.top, self.bottom, self.left, self.right
        size = self._size
        last = size - 1

        edge = []

        for k in range(depth):
            top_edge = [top[i][k] for i in range(size)]
            right_edge = [right[last-k][i] for i in reversed(range(size))]
            bottom_edge = [bottom[i][last-k] for i in reversed(range(size))]
            left_edge = [left[k][i] for i in range(size)]
            edge.extend(top_edge + right_edge + bottom_edge + left_edge)

        return edge

    def _set_outer_edge(self, depth, values):
        """Set outer edge squares up to depth"""

        top, bottom, left, right = self.top, self.bottom, self.left, self.right

        size = self._size
        last = size - 1
        size_range = range(self._size)

        for k in range(depth):
            for i in size_range:
                offset = k * 4 * size
                top[i][k] = values[offset + i]
                # right[last-k][i] = values[offset + 5 - i]
                # bottom[i][last-k] = values[offset + 8 - i]
                # left[k][i] = values[offset + 9 + i]
                right[last-k][i] = values[offset + size+last - i]
                bottom[i][last-k] = values[offset + 2*size+last - i]
                left[k][i] = values[offset + 3*size + i]


    def rotate(self, direction, depth=1):
        """Rotate face up to deph

        direction is either 'left' or 'right'
        depth should be between 1 and half the cube's size (edge length)
        """

        size = self._size

        if not 1 <= depth <= (max_depth := size // 2):
            raise ValueError(f"Rotation depth must be between 1 and {max_depth} "
                             f"for {size}x{size}x{size} Rubik's cube")

        inner_edge_colors = deque(self.inner_edge)
        outer_edge_colors = deque(self._get_outer_edge(depth))

        if direction.lower() == 'left':
            inner_edge_colors.rotate(-size+1)
            outer_edge_colors.rotate(-size)
        elif direction.lower() == 'right':
            inner_edge_colors.rotate(size-1)
            outer_edge_colors.rotate(size)
        else:
            raise ValueError('direction must be "left" or "right"')

        self.inner_edge = inner_edge_colors
        self._set_outer_edge(depth, outer_edge_colors)

    def all_same_color(self):
        """Check if all the face's squares are the same color"""
        size_range = range(self._size)
        squares = self._squares
        color = squares[0][0]
        for i in size_range:
            for j in size_range:
                if squares[i][j] != color:
                    return False
        return True

    def reset_color(self):
        """Switch the squares' color to that of the center square"""
        size_range = range(self._size)
        initial_color = self._initial_color
        for i in size_range:
            for j in size_range:
                self[i][j] = initial_color


class RubiksCube:
    """Python class representing a Rubik's cube

    size is the cube's edge length
    """

    COLORS = ['red', 'blue', 'green', 'yellow', 'white', 'orange']

    __slots__ = ['_size', '_faces'] + COLORS

    def __init__(self, size=3) -> None:

        if size < 2:
            raise ValueError('Cube size must be at least 2')

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
    print('Cube after scramble:')
    print(cube)
    print('Cube is solved after scramble:', cube.is_solved())

    print(50 * '*')

    # Reset the cube
    cube.reset()
    print('Cube after reset:')
    print(cube)
    print('Cube is solved after reset:', cube.is_solved())

    # 4x4x4 cube
    cube4 = RubiksCube(4)
    cube4.blue.rotate('right', 2)
    print('4x4x4 cube after right 2-rotation:')
    print(cube4)
    cube4.blue.rotate('left', 1)
    print('4x4x4 cube after left 1-rotation:')
    print(cube4)

    try:
        cube4.blue.rotate('left', 7)
    except ValueError as e:
        print(f'Large rotation depth error message: {e.args[0]}')
