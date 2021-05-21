from collections.abc import Iterable
from types import GeneratorType

from .dictlist import DictList


class TupleDict(dict):
    """
    Somewhat inspired by Anton Dries https://pypi.org/project/tupledict/
    """

    def __init__(self, *args, **kwargs):
        self._key_len = None
        self._key_indx = {}
        super().__init__()
        if args:
            if len(args) > 1:
                raise TypeError(f"Expected at most 1 arguments, got {len(args)}")
            arg = args[0]
            if isinstance(arg, dict):
                self.update({self._valid_key(k): v for k, v in arg.items()})
            elif isinstance(arg, Iterable):
                self.update(((self._valid_key(k), v) for k, v in arg))
        if kwargs:
            self.update({self._valid_key(k): v for k, v in kwargs.items()})
        for k, v in self.items():
            self._add_indx_key(k, v)

    def __setitem__(self, key, value):
        key = self._valid_key(key)
        super().__setitem__(key, value)
        self._add_indx_key(key, value)

    def __getitem__(self, key):
        key = self._valid_key(key)
        return super().__getitem__(key)

    def select(self, *keys):
        key = tuple(keys)
        key = self._valid_key(key)
        if any(
            v == "*" or isinstance(v, list) or isinstance(v, GeneratorType) for v in key
        ):
            tmp = self._key_indx
            for k in key[:-1]:
                if k == "*":
                    # wildcard
                    tmp = DictList(tmp.values())
                elif isinstance(k, list) or isinstance(k, GeneratorType):
                    tmp = DictList([v for kee, v in tmp.items() if kee in k])
                else:
                    tmp = tmp[k]
            if key[-1] == "*":
                # wildcard
                return list(tmp.values())
            elif isinstance(key[-1], list) or isinstance(key[-1], GeneratorType):
                return [v for k, v in tmp.items() if k in key[-1]]
            else:
                return tmp[key[-1]]
        else:
            return self.__getitem__(key)

    def _valid_key(self, key):
        if not isinstance(key, tuple):
            key = (key,)
        self._check_key_len(len(key))
        return key

    def _check_key_len(self, key_len):
        if self._key_len is None:
            self._key_len = key_len
        elif self._key_len != key_len:
            raise KeyError(
                f"Key length is {key_len} but this dict has key length {self._key_len}."
            )

    def _add_indx_key(self, key, value):
        """
        Read the test.
        """
        tmp = self._key_indx
        for k in key[:-1]:
            # worth trying this I think
            # tmp[k] = tmp.get(k, {})
            if k not in tmp:
                tmp[k] = {}
            tmp = tmp[k]
        tmp[key[-1]] = value
