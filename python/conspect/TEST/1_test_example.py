import pytest 

def add(a, b): 
    return a + b

def test_math():
    assert add(2, 3) == 5

def test_list_diff():
    assert [1, 2, 3] == [1, 2, 4]   # покажет diff, что отличается последний элемент

def test_str_diff():
    assert "hello\nworld" == "hello\nWorld"  # построчный дифф с подсветкой