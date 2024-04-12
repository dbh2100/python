"""This module defines a Python representation of a Rubik's cube"""

from collections import deque

class _RubiksCubeFace:

    __slots__ = ['_squares', 'top', 'bottom', 'left', 'right']

    def __init__(self, color) -> None:

        squares = []
        for _ in range(3):
            squares.append(3 * [color])
        self._squares = squares

        # Set adjacent squares in RubiksCube initializer
        self.top, self.bottom, self.left, self.right = None, None, None, None

    def __repr__(self) -> str:
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
        return len(set(self[0] + self[1] + self[2])) == 1


class RubiksCube:
    """Python class representing a Rubik's cube"""

    __slots__ = ['faces']

    def __init__(self) -> None:
        colors = ['R', 'B', 'G', 'Y', 'W', 'O']
        self.faces = [_RubiksCubeFace(color) for color in colors]
        self.set_adjacent(*self.faces)

    def set_adjacent(self, target_face, top, bottom, left, right, back):
        """Recursively set the adjacent faces for the target face
        and the other cube faces
        """

        target_face.top = top
        target_face.bottom = bottom
        target_face.left = left
        target_face.right = right

        # Check if top.left and bottom.right are already set to avoid infinite recursion
        if top.left is None:
            self.set_adjacent(top, left, right, target_face, back, bottom)
        if bottom.right is None:
            self.set_adjacent(bottom, right, left, back, target_face, top)

    def is_solved(self):
        """Determine if all squares on each face have same color"""
        return all(face.all_same_color() for face in self.faces)


if __name__ == '__main__':

    cube = RubiksCube()
    print(cube.is_solved())

    cube.faces[0].rotate('left')
    for face in cube.faces:
        print(face)
    print(cube.is_solved())

    print(50 * '*')

    cube.faces[0].rotate('right')
    for face in cube.faces:
        print(face)
    print(cube.is_solved())

    for i, face in enumerate(cube.faces):
        for attr in ['top', 'bottom', 'left', 'right']:
            print(i, attr, hasattr(face, attr))
