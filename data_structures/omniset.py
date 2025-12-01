"""Define a set containing all possible elements."""

from singleton import Singleton


class Omniset(frozenset, Singleton):
    """Class for a set containing all elements other than itself."""

    def __init__(self, *args, **kwargs) -> None:
        # Should not be able to pass arguments to constructor
        if args or kwargs:
            raise ValueError(f'{self.__class__.__name__} does not take any arguments.')
        super().__init__()

    def __contains__(self, element: object) -> bool:
        return element is not self
