"""Defines a base class for singleton pattern implementation."""


class SingletonMeta(type):
    """A metaclass for singleton pattern implementation."""

    _instances: dict[type, object] = {}

    def __call__(cls, *args, **kwargs):

        # Should not be able to pass arguments to constructor
        if args or kwargs:
            raise TypeError(f'{cls.__name__} does not take any arguments.')

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """A base class for singleton pattern implementation."""
    pass
