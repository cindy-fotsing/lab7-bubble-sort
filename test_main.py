import pytest

from main import bubble_sort


def test_bubble_sort_returns_sorted_numbers():
    data = [4, 1, 3, 10, 5, 16, 2]
    result = bubble_sort(data, in_place=False)
    assert result == [1, 2, 3, 4, 5, 10, 16]


def test_bubble_sort_handles_duplicates():
    data = [3, 1, 2, 3, 2]
    result = bubble_sort(data, in_place=False)
    assert result == [1, 2, 2, 3, 3]


def test_bubble_sort_mutates_input_when_in_place_true():
    data = [5, 4, 1]
    result = bubble_sort(data, in_place=True)
    assert data == [1, 4, 5]
    assert result is data


def test_bubble_sort_keeps_input_unchanged_when_in_place_false():
    data = [5, 4, 1]
    result = bubble_sort(data, in_place=False)
    assert data == [5, 4, 1]
    assert result == [1, 4, 5]


def test_bubble_sort_raises_type_error_for_non_comparable_values():
    with pytest.raises(TypeError):
        bubble_sort([1, "a"], in_place=False)
