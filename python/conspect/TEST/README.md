###### PYTEST
```
pip install pytest
```
###### запуск  
```
# запустит тесты в файлах начинающихся test_*
run pytest -vv TEST/test_example.py
# c указанием версии python
run --python 3.12 pytest -vv TEST/test_example.py

run pytest 			         # стандартный запуск
run pytest -q 			     # тише
run pytest -vv 			     # подробные имена кейсов
run pytest -k sum 		     # фильтр по выражению/подстроке имени теста
run pytest -m "not slow" 	 # запуск без помеченных slow
run pytest -x --maxfail=1 	 # остановиться на первом падении
```
```
project/
├─ src/ # Ваш исходный код (опционально)
├─ app/ # Или пакет приложения (Flask, etc.)
├─ tests/ # Все тесты здесь
│ ├─ test_smoke.py
│ ├─ test_api.py
│ └─ conftest.py # Общие фикстуры/хуки для tests/
└─ pytest.ini # Конфигурация pytest
```
pyproject.toml

```tolm 
[tool.pytest.ini_options]
minversion = "6.0"
testpaths = ["tests"]
python_files = test_*.py *_test.py
python_functions = test_*
addopts = [
  "-vv",				        # подробный вывод хода теста
  "--import-mode=importlib"  	# меньше проблем с импортами
]
```
```
правила обнаружения тестов: файлы test_*.py или _test.py, функции test_, классы Test* без init.py
- Каталог с тестами должен называться tests
- Названия файлов тестов должны начинаться с test, например test_basic.py, либо заканчиваться на test.py
- Названия функций тестов должны начинаться с test_, например def test_simple():
- Названия классов тестов должны начинаться на Test, например class TestSimple
- Методы тестов придерживаются тех же соглашений, что и функции, и должны начинаться на test_, например, def test_method(self):.

```
##### Написание теста 

```
cd TEST

test_example.py
```
```python 

import pytest 

def add(a, b): 
    return a + b

def test_math():
    assert add(2, 3) == 5
```

```python 
# assert проверяет, является ли выражение истинным
def test_simple():
    assert True     # True Истина - тест проходит
def test_fails():
    assert False    # False не явлется истиной - тест проваливается
```
##### Параметризация тестов

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (2, 5, 7),
    (-1, 1, 0),
],
ids=["first_row 1 1 2", "second_row 2 5 7", "third_row -1 1 0"])
)
def test_add(a, b, expected):
    assert a + b == expected

```
###### Параметризация тестов
pytest -vv 2_test_example.py 

###### В качестве имени кейса можно передать функцию. Такая функция получает значение параметра и должна вернуть строку-имя кейса.

pytest -vv 3_test_example.py 


###### Метки и фильтрация
```
Для создания групп тестов можно использовать специальные средства в pytest - маркеры. Они позволяют выбирать/исключать тесты при запуске
Задается список маркеров в файле проекта  pyproject.toml в секции [tool.pytest.ini_options]
```
```
markers = [
    "slow: долгие тесты",
    "integration: интеграционные тесты",
    "network: сетевые тесты"
]
```
```
запустить "медленные" тесты и без сетевых
```
```
pytest -m "slow and not network" 4_test_example.py 
```

###### Параметризация
```
pytest -vv 5_test_example.py 
```
###### conftest.py

```
место где складываются “элементы инфраструктуры” для выполнения тестов на уровне текущей директории.

```

###### Фикстуры
```
 маленькие вспомогательные функции, внедряемые в тест
```