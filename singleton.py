"""Defines a base class for singleton pattern implementation."""


from __future__ import annotations


class SingletonMeta(type):
    """A metaclass for singleton pattern implementation."""

    _instances: dict[SingletonMeta, object] = {}

    def __call__(cls: SingletonMeta) -> object:

        if cls not in cls._instances:
            instance = super().__call__()
            cls._instances[cls] = instance

        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """A base class for singleton pattern implementation."""
    pass
