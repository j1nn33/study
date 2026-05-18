###### PYTEST
```
pip install pytest

запуск 

pytest ./python/conspect/TEST/test_basic.py 
или  
/repo/study/python/conspect/TEST$ pytest -vv 
# запустит тесты в файлах начинающихся
test_*

- Каталог с тестами должен называться tests
- Названия файлов тестов должны начинаться с test, например test_basic.py, либо заканчиваться на test.py
- Названия функций тестов должны начинаться с test_, например def test_simple():
- Названия классов тестов должны начинаться на Test, например class TestSimple
- Методы тестов придерживаются тех же соглашений, что и функции, и должны начинаться на test_, например, def test_method(self):.

```

```python 
# assert проверяет, является ли выражение истинным
def test_simple():
    assert True     # True Истина - тест проходит
def test_fails():
    assert False    # False не явлется истиной - тест проваливается
```
```
============ test session starts 
==========   FAILURES 
_______ test_fails ______
    def test_fails():
>       assert False
E       assert False

python/conspect/TEST/test_basic.py:4: AssertionError

====== short test summary info 

FAILED python/conspect/TEST/test_basic.py::test_fails - assert False

======= 1 failed, 1 passed in 0.05s 
```