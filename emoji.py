"""Python emoji class"""

class EmojiMeta(type):
    """Metaclass for Emoji class"""

    # Use dot access to get emoji
    def __getattr__(cls, name):
        if name in cls._instances:
            return cls._instances[name]
        return super().__getattribute__(name)

    # Include each emoji name in dir()
    # Useful for accessing emoji in an IDE
    def __dir__(cls):
        return list(super().__dir__()) + list(cls._instances)

class Emoji(metaclass=EmojiMeta):
    """Python emoji class

    >>> from emoji import Emoji
    >>> Emoji.register_or_update('smile', ':)')
    >>> Emoji('smile')
    :)
    >>> Emoji.smile
    :)
    """

    # Map of emoji name to instance
    _instances = {}

    @classmethod
    def register_or_update(cls, name, picture):
        """Use this to add emoji with name and pictoral representation picture

        or to update the pictoral representation for an existing emoji
        """
        inst = super().__new__(cls)
        inst.name = name
        inst._picture = picture
        cls._instances[name] = inst

    def __new__(cls, name):
        if name not in cls._instances:
            raise ValueError(f'Emoji "{name}" not registered yet')
        return cls._instances[name]

    def __repr__(self):
        return self._picture


if __name__ == '__main__':
    import doctest
    doctest.testmod()
