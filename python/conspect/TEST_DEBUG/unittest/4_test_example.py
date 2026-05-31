import pytest 

def add(a, b): 
    return a + b

@pytest.mark.slow
def test_long():
    assert add(2, 3) == 5

@pytest.mark.integration
def test_needs_device():
    assert [1, 2, 3] == [1, 2, 3]

@pytest.mark.network
def test_bug():
    assert 1 == 2