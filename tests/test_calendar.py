import pytest

from cli_cqu.util.calendar import make_range


@pytest.mark.parametrize("r, ex", [
    ("1", [1]),
    ("1-14", [(1, 14)]),
    ("1,3", [1, 3]),
    ("1-9,11-14", [(1, 9), (11, 14)]),
    ("1,3-9", [1, (3, 9)]),
])
def test_make_range(r, ex):
    assert make_range(r) == ex
