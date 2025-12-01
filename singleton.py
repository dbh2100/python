"""Defines a base class for singleton pattern implementation."""


class SingletonMeta(type):
    """A metaclass for singleton pattern implementation."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """A base class for singleton pattern implementation."""
    pass
