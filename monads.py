"""This module defines several monads using Python"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union, Optional, TypeVar, Generic
from collections.abc import Callable


Numeric = Union[complex, float, int]

T = TypeVar('T')
N = TypeVar('N', complex, float, int)


@dataclass
class Maybe(Generic[T]):
    """The Maybe monad"""
    value: Optional[T]

    def bind(self, func: Callable[[T], Optional[T]]) -> Maybe[T]:
        """Binds a function"""
        if self.value is None:
            return self
        return Maybe(func(self.value))


@dataclass
class NumberWithLogs:
    """This monad logs the application of a function to a number"""
    value: Numeric
    logs: list[str] = field(default_factory=list[str])

    def bind(self, func: Callable[[Numeric], Numeric]) -> NumberWithLogs:
        """Binds a numeric function"""
        result = func(self.value)
        new_log = f'Applying {func.__name__}() to {self.value}'
        return NumberWithLogs(result, self.logs + [new_log])


def add_five(x: N) -> N:
    """Adds 5 to the input"""
    return x + 5

def cube(x: N) -> N:
    """Cubes the input"""
    return x ** 3

def sub_3(x: N) -> N:
    """Subtracts 3 from the input"""
    return x - 3

def divide_into_seven(x: N) -> Optional[N]:
    """Divides 7 by the input"""
    try:
        return 7 // x if isinstance(x, int) else 7 / x
    except ZeroDivisionError:
        return None


if __name__ == '__main__':

    print('Testing Maybe monad...')
    result1 = Maybe(-2).bind(add_five).bind(divide_into_seven).bind(cube)
    print(f'{result1 = }')
    result2 = Maybe(-2).bind(add_five).bind(sub_3).bind(divide_into_seven).bind(cube)
    print(f'{result2 = }')
    print()

    print('Testing NumberWithLogs monad...')
    result3 = NumberWithLogs(11).bind(add_five).bind(cube).bind(sub_3)
    for log in result3.logs:
        print(log)
    print(f'The final value is {result3.value}')
