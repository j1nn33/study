import pytest

def setup_module(module):
    #init_something()
    pass

def teardown_module(module):
    #teardown_something()
    pass

def test_upper():
    assert 'foo'.upper() == 'FOO'
    
def test_isupper():
    assert 'FOO'.isupper()
    
def test_failed_upper():
    assert 'foo'.upper() == 'FOo'
    
    
#+++++++++++++++++++++++
"""
(venv) D:\SOURCE\python\ipython>py.test -s -v  \SOURCE\python\ipython\venv\ipython.py
============================= test session starts =============================
platform win32 -- Python 3.6.2, pytest-3.5.1, py-1.5.3, pluggy-0.6.0 -- d:\source\python\ipython\venv\scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\SOURCE\python\ipython, inifile:
collected 3 items                                                              

venv/ipython.py::test_upper PASSED
venv/ipython.py::test_isupper PASSED
venv/ipython.py::test_failed_upper FAILED

================================== FAILURES ===================================
______________________________ test_failed_upper ______________________________

    def test_failed_upper():
>       assert 'foo'.upper() == 'FOo'
E       AssertionError

venv\ipython.py:23: AssertionError
===================== 1 failed, 2 passed in 0.11 seconds ======================

"""