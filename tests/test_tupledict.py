from typing import Any, List, Tuple
from unittest import mock

import pytest

from tupledict import TupleDict


class TestTupleDict:
    def test__init__(self) -> None:
        td: TupleDict

        # no args
        td = TupleDict()
        assert td._key_len is None
        assert td._key_indx == {}
        assert td == {}

        # meaningless arg (not dict or iterable)
        td = TupleDict(1)
        assert td._key_len is None
        assert td._key_indx == {}
        assert td == {}

        # too many args
        with pytest.raises(TypeError, match=".* got 2"):
            td = TupleDict(1, 2)

        # dict arg
        td = TupleDict({"one": 1, "two": 2})
        assert td._key_len == 1
        assert td._key_indx == {"one": 1, "two": 2}
        assert td == {("one",): 1, ("two",): 2}

        # iterable arg
        td = TupleDict([("one", 1), ("two", 2)])
        assert td._key_len == 1
        assert td._key_indx == {"one": 1, "two": 2}
        assert td == {("one",): 1, ("two",): 2}

        # kwargs
        td = TupleDict(one=1, two=2)
        assert td._key_len == 1
        assert td._key_indx == {"one": 1, "two": 2}
        assert td == {("one",): 1, ("two",): 2}

        # mixed
        td = TupleDict({"one": 1, "two": 2}, three=3, four=4)
        assert td._key_len == 1
        assert td._key_indx == {"one": 1, "two": 2, "three": 3, "four": 4}
        assert td == {("one",): 1, ("two",): 2, ("three",): 3, ("four",): 4}

        with mock.patch(
            "tupledict.TupleDict._valid_key", return_value=("one",)
        ) as mock_valid_key:
            # dict arg
            td = TupleDict({"one": 1})
            mock_valid_key.assert_called_once_with("one")

            # iterable arg
            mock_valid_key.reset_mock()
            td = TupleDict([("one", 1)])
            mock_valid_key.assert_called_once_with("one")
            # kwarg
            mock_valid_key.reset_mock()
            td = TupleDict(one=1)
            mock_valid_key.assert_called_once_with("one")

        with mock.patch(
            "tupledict.TupleDict._add_indx_key", return_value=None
        ) as mock_add_indx_key:
            td = TupleDict({"one": 1, "two": 2}, three=3, four=4)
            mock_add_indx_key.assert_has_calls(
                [
                    mock.call(("one",), 1),
                    mock.call(("two",), 2),
                    mock.call(("three",), 3),
                    mock.call(("four",), 4),
                ],
                any_order=True,
            )

    def test__setitem__(self) -> None:
        td: TupleDict = TupleDict()
        td["one"] = 1
        assert td._key_len == 1
        assert td._key_indx == {"one": 1}
        assert td == {("one",): 1}

        td["two"] = 2
        assert td._key_len == 1
        assert td._key_indx == {"one": 1, "two": 2}
        assert td == {("one",): 1, ("two",): 2}

        # len(key) != 1
        with pytest.raises(KeyError, match=(".* 2 .* 1.")):
            td[("three", "four")] = 34

        with mock.patch.object(
            td, "_valid_key", return_value=("one",)
        ) as mock_valid_key:
            td["one"] = 1
            mock_valid_key.assert_called_once_with("one")

        td = TupleDict({"one": 1})
        assert td._key_len == 1
        assert td._key_indx == {"one": 1}
        assert td == {("one",): 1}

        td["one"] = 2
        assert td._key_len == 1
        assert td._key_indx == {"one": 2}
        assert td == {("one",): 2}

    @pytest.mark.parametrize(
        "init, key, expected, raises",
        [
            ([], "one", None, True),
            ([("one", 1), ("two", 2)], "one", 1, False),
            ([("one", 1), ("two", 2)], ("one",), 1, False),
            ([("one", 1), ("two", 2)], "two", 2, False),
            ([("one", 1), ("two", 2)], ("two",), 2, False),
            ([("one", 1), ("two", 2)], "three", None, True),
            ([("one", 1), ("two", 2)], ("three", "four"), None, True),
        ],
    )
    def test__getitem__(
        self, init: List[Tuple[Any, Any]], key: Any, expected: Any, raises: bool
    ) -> None:
        td: TupleDict = TupleDict(init)
        if raises:
            with pytest.raises(KeyError):
                td[key]
        else:
            assert td[key] == expected

    @pytest.mark.parametrize(
        "init, select_args, expected, raises",
        [
            ([], ("one",), None, True),
            ([("one", 1), ("two", 2)], ("one",), 1, False),
            ([("one", 1), ("two", 2)], ("two",), 2, False),
            ([("one", 1), ("two", 2)], ("*",), [1, 2], False),
            (
                [(("one", "two"), 12), (("one", "three"), 13), (("two", "three"), 23)],
                ("one",),
                None,
                True,
            ),
            (
                [(("one", "two"), 12), (("one", "three"), 13), (("two", "three"), 23)],
                ("one", "two"),
                12,
                False,
            ),
            (
                [(("one", "two"), 12), (("one", "three"), 13), (("two", "three"), 23)],
                ("*", "three"),
                [13, 23],
                False,
            ),
        ],
    )
    def test_select(
        self,
        init: List[Tuple[Any, Any]],
        select_args: Tuple[Any, ...],
        expected: Any,
        raises: bool,
    ) -> None:
        td: TupleDict = TupleDict(init)
        if raises:
            with pytest.raises(KeyError):
                td.select(*select_args)
        else:
            assert td.select(*select_args) == expected

    def test_valid_key(self) -> None:
        td: TupleDict = TupleDict()
        assert td._valid_key("one") == ("one",)
        assert td._valid_key(("two",)) == ("two",)
        assert td._key_len == 1

        with mock.patch.object(
            td, "_check_key_len", return_value=None
        ) as mock_chk_key_len:
            td._valid_key("three")
            mock_chk_key_len.assert_called_once_with(1)
            mock_chk_key_len.reset_mock()
            td._valid_key(("four", "five"))
            mock_chk_key_len.assert_called_once_with(2)

    def test_check_key_len(self) -> None:
        td: TupleDict = TupleDict()
        assert td._key_len is None
        td._check_key_len(5)
        assert td._key_len == 5

        with pytest.raises(KeyError, match=(".* 4 .* 5.")):
            td._check_key_len(4)

        td = TupleDict([("one", 1), ("two", 2)])
        assert td._key_len == 1

        with pytest.raises(KeyError, match=(".* 5 .* 1.")):
            td._check_key_len(5)

    def test_add_indx_key(self) -> None:
        td: TupleDict = TupleDict()
        td._add_indx_key(("one",), 1)
        assert td._key_indx == {"one": 1}

        td = TupleDict()
        td._add_indx_key(("one", "two"), 12)
        assert td._key_indx == {"one": {"two": 12}}

        td._add_indx_key(("one", "three"), 13)
        assert td._key_indx == {"one": {"two": 12, "three": 13}}

        td._add_indx_key(("two", "three"), 23)
        assert td._key_indx == {"one": {"two": 12, "three": 13}, "two": {"three": 23}}

    def test_len_and_iteration(self) -> None:
        td: TupleDict = TupleDict([("a", 1), ("b", 2)])
        assert len(td) == 2
        assert set(td) == {("a",), ("b",)}
        assert set(td.values()) == {1, 2}

    def test_delitem(self) -> None:
        td: TupleDict = TupleDict([("a", 1)])
        del td[("a",)]
        assert len(td) == 0
        assert td._key_indx == {}

    def test_invalid_key_type(self) -> None:
        td: TupleDict = TupleDict()
        with pytest.raises(TypeError):
            td[{1, 2}] = 3  # set is unhashable

    def test_equality(self) -> None:
        td1: TupleDict = TupleDict([("a", 1)])
        td2: TupleDict = TupleDict([("a", 1)])
        assert td1 == td2
        td2["b"] = 2
        assert td1 != td2
