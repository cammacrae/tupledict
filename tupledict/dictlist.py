from itertools import chain


class DictList:
    """
    Inspired by Anton Dries https://pypi.org/project/tupledict/
    """

    def __init__(self, indx):
        self._indx = indx

    def __getitem__(self, key):
        return [d[key] for d in self._indx if key in d]

    def values(self):
        return list(chain(*(d.values() for d in self._indx)))

    def items(self):
        return list(chain(*(d.items() for d in self._indx)))
