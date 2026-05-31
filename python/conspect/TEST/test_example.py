import pytest 

def add(a, b): 
    return a + b

def test_math():
    assert add(2, 3) == 5