from itertools import chain
from typing import Dict, Generic, Iterable, List, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class DictList(Generic[K, V]):
    """
    Inspired by Anton Dries https://pypi.org/project/tupledict/
    """

    def __init__(self, indx: Iterable[Dict[K, V]]) -> None:
        self._indx: Iterable[Dict[K, V]] = indx

    def __getitem__(self, key: K) -> List[V]:
        return [d[key] for d in self._indx if key in d]

    def values(self) -> List[V]:
        return list(chain(*(d.values() for d in self._indx)))

    def items(self) -> List[Tuple[K, V]]:
        return list(chain(*(d.items() for d in self._indx)))
