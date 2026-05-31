import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (2, 5, 7),
    (-1, 1, 0),
],
ids=["first", "second", "third"])

def test_add(a, b, expected):
    assert a + b == expected