from collections.abc import Mapping
from typing import Any, Iterator

class FrozenDict(Mapping):

    def __init__(self, *args, **kwargs) -> None:
        self._dict = dict(*args, **kwargs)

    def __getitem__(self, __key: Any) -> Any:
        return self._dict.__getitem__(__key)

    def __iter__(self) -> Iterator:
        return self._dict.__iter__()

    def __len__(self) -> int:
        return self._dict.__len__()

    @classmethod
    def fromkeys(cls, *args, **kwargs):
        return cls(dict.fromkeys(*args, **kwargs))

    def __hash__(self) -> int:
        return hash(tuple(self.items()))

    def __repr__(self) -> str:
        return '%s(%s)' % self.__class__.__name__, self._dict
