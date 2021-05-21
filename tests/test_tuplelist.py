import pytest
from tupledict import DictList


class TestDictList:
    def test__init__(self):
        dl = DictList([{}])
        assert dl._indx == [{}]

    @pytest.fixture
    def dictlist(self):
        dl = DictList(
            [{"one": 1, "two": 2}, {"one": 1.1, "two": 2.1, "three": {"four": 4}}]
        )
        return dl

    def test__getitem__(self, dictlist):
        assert dictlist.__getitem__("one") == [1, 1.1]
        assert dictlist["one"] == [1, 1.1]
        assert dictlist["three"] == [{"four": 4}]

    def test_values(self, dictlist):
        assert dictlist.values() == [1, 2, 1.1, 2.1, {"four": 4}]

    def test_items(self, dictlist):
        assert dictlist.items() == [
            ("one", 1),
            ("two", 2),
            ("one", 1.1),
            ("two", 2.1),
            ("three", {"four": 4}),
        ]
