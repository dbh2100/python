"""This module defines functions involving Pascal's triangle"""

import itertools
from numbers import Integral
from functools import lru_cache


def gen_pascal():
    """Generate the rows of Pascal's trangle"""
    row = [1]
    row_num = 1
    while True:
        yield row
        prev_row = row
        row_num += 1
        row = []
        for col in range(row_num):
            num1 = 0 if col == 0 else prev_row[col-1]
            num2 = 0 if col == (row_num-1) else prev_row[col]
            row.append(num1 + num2)


def gen_pascal_tee():
    """Generate the rows of Pascal's trangle using tee from itertools"""

    def _row_gen():
        yield [1]
        row_num = 1
        while True:
            try:
                prev_row = next(prev_row_gen)
            except StopIteration:
                return
            next_row = [1]
            for col in range(1, row_num):
                next_row.append(prev_row[col-1] + prev_row[col])
            next_row.append(1)
            yield next_row
            row_num += 1

    row_it = _row_gen()
    prev_row_gen, row_gen = itertools.tee(row_it)
    return row_gen


@lru_cache(maxsize=None)
def pascal(row, column):
    """Return the number in the specified row and column
    from Pascal's triangle"""

    assert isinstance(row, Integral) and row >= 0
    assert isinstance(column, Integral) and 0 <= column <= row

    if column in (0, row):
        return 1

    return pascal(row-1, column-1) + pascal(row-1, column)


if __name__ == '__main__':

    NUM_ROWS = 15

    for gen_func in [gen_pascal, gen_pascal_tee]:
        pascal_gen = gen_func()
        print(f"Generating the first {NUM_ROWS} rows of Pascal's triangle "
              f"from {gen_func.__name__}():")
        for _ in range(NUM_ROWS):
            print(next(pascal_gen))
        print()

    print(f"Generating the first {NUM_ROWS} rows of Pascal's triangle "
          "from pascal():")
    for i in range(NUM_ROWS):
        print([pascal(i, j) for j in range(i+1)])
