from typing import Any, List

import pytest

from tupledict import DictList


class TestDictList:
    def test__init__(self) -> None:
        dl: DictList = DictList([{}])
        assert dl._indx == [{}]

    @pytest.fixture
    def dictlist(self) -> DictList:
        dl: DictList = DictList(
            [{"one": 1, "two": 2}, {"one": 1.1, "two": 2.1, "three": {"four": 4}}]
        )
        return dl

    @pytest.mark.parametrize(
        "key,expected",
        [
            ("one", [1, 1.1]),
            ("three", [{"four": 4}]),
        ],
    )
    def test__getitem__(
        self, dictlist: DictList, key: str, expected: List[Any]
    ) -> None:
        assert dictlist.__getitem__(key) == expected
        assert dictlist[key] == expected

    def test_values(self, dictlist: DictList) -> None:
        assert dictlist.values() == [1, 2, 1.1, 2.1, {"four": 4}]

    def test_items(self, dictlist: DictList) -> None:
        assert dictlist.items() == [
            ("one", 1),
            ("two", 2),
            ("one", 1.1),
            ("two", 2.1),
            ("three", {"four": 4}),
        ]
