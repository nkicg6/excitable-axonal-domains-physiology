import pytest
from patch_clamp import database


def test_list_of_ints_to_str():
    list_ints = [1, 2, 3, 4]
    l_str = database.list_of_ints_to_str(list_ints)
    assert "1,2,3,4" == l_str


def test_str_list_to_list_ints():
    string_ints = "1,2,3,4"
    converted = database.str_list_to_list_ints(string_ints)
    assert [1, 2, 3, 4] == converted


def test_list_to_ints_and_back():
    list_ints = [1, 2, 3, 4]
    l_str = database.list_of_ints_to_str(list_ints)
    decoded = database.str_list_to_list_ints(l_str)
    assert list_ints == decoded


def test_assertion_throw_float_in_ints():
    string_with_float = "1,2,3.5,4"
    with pytest.raises(ValueError):
        database.str_list_to_list_ints(string_with_float)


def test_list_to_ints_and_back_empty_list():
    list_empty = []
    l_str = database.list_of_ints_to_str(list_empty)
    decoded = database.str_list_to_list_ints(l_str)
    assert list_empty == decoded
