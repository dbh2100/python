"""Define a set containing all possible elements."""

from __future__ import annotations
from singleton import Singleton
from collections.abc import Iterable


class Omniset(frozenset, Singleton):
    """Class for a set containing all elements other than itself."""

    def __contains__(self, element: object) -> bool:
        return element is not self

    def __len__(self) -> int:
        raise OverflowError("The omniset has no finite length.")

    def issubset(self, other: Iterable[object], /) -> bool:
        """Check if the omniset is a subset of another set"""
        return other is self

    def issuperset(self, s: Iterable[object]) -> bool:
        """Check if the omniset is a superset of another set"""
        return True

    def union(self, *others) -> Omniset:
        """Override union to always return the omniset"""
        return self

    def intersection(self, *others) -> frozenset:
        """Override intersection to return the other set(s)"""

        if not others:
            return self

        return_set = set(others[0])
        for other in others[1:]:
            return_set.intersection_update(other)
        return frozenset(return_set)
