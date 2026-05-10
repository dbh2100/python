"""This module defines several monads using Python

The Maybe monad is used to handle computations that may fail, while the
NumberWithLogs monad is used to log the application of functions to numbers.
The module also includes some example functions and demonstrates how to use
these monads in a simple way.

Binding is implemented using the right shift operator (>>), which allows for
chaining operations in a clean and readable manner. The example functions include
adding five, cubing a number, subtracting three, and dividing seven by a number,
with appropriate handling for division by zero in the Maybe monad.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, TypeVar, Generic, Protocol, runtime_checkable
from collections.abc import Callable


T = TypeVar('T')
N = TypeVar('N', complex, float, int)


@runtime_checkable
class Monad(Protocol[T]):
    """A protocol for monads, defining the bind operation"""

    def __rshift__(self, func: Callable[[T], T]) -> Monad[T]:
        """The bind operation, which applies a function to the value inside the monad"""
        ...


@dataclass
class Maybe(Generic[T]):
    """The Maybe monad

    This monad is used to handle computations that may fail. If a computation fails,
    the value is set to None and subsequent operations will not be applied.

    Example usage:
    >>> result = Maybe(-2) >> add_five >> divide_into_seven >> cube
    >>> print(result)
    Maybe(value=8)
    >>> result = Maybe(0) >> divide_into_seven
    >>> print(result)
    Maybe(value=None)
    """

    value: Optional[T]

    def __rshift__(self, func: Callable[[T], Optional[T]]) -> Maybe[T]:
        if self.value is None:
            return self
        return Maybe(func(self.value))


@dataclass
class NumberWithLogs(Generic[N]):
    """This monad logs the application of a function to a number
    
    Example usage:
    >>> result = NumberWithLogs(10) >> add_five >> cube
    >>> for log in result.logs:
    ...     print(log)
    Applying add_five() to 10
    Applying cube() to 15
    >>> print(result.value)
    3375
    """

    value: N
    logs: list[str] = field(default_factory=list[str])

    def __rshift__(self, func: Callable[[N], N]) -> NumberWithLogs[N]:
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
    print(f'Maybe is a monad: {isinstance(Maybe(0), Monad)}')
    result1 = Maybe(-2) >> add_five >> divide_into_seven >> cube
    print(f'{result1 = }')
    result2 = Maybe(-2) >> add_five >> sub_3 >> divide_into_seven >> cube
    print(f'{result2 = }')
    print()

    print('Testing NumberWithLogs monad...')
    print(f'NumberWithLogs is a monad: {isinstance(NumberWithLogs(0), Monad)}')
    result3 = NumberWithLogs(11) >> add_five >> cube >> sub_3
    for log in result3.logs:
        print(log)
    print(f'The final value is {result3.value}')
