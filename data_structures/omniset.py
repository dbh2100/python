"""Define a set containing all possible elements."""

from singleton import Singleton


class Omniset(frozenset, Singleton):
    """Class for a set containing all elements other than itself."""

    def __contains__(self, element: object) -> bool:
        return element is not self
