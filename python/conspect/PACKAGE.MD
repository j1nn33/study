#### Пакеты

```
старшая.младшая.микро
x.y.z

x- старшая версия — для обратно несовместимых изменений;
y - младшая версия включает в ПО обратно совместимую функциональность;
z - микроверсия включает в ПО обратно совместимые исправления ошибок.

журнал изменений 
четыре важных элемента информации.
1. Номер последней выпущенной версии.
2. Совместима ли обратно последняя выпущенная версия.
3. Дата выхода последней версии.
4. Включенные в этот выпуск изменения.
```

создание виртуального окружениея
```
mkdir new_dir
cd new_dir
python -m venv my_new_environment

# В этой команде my_new_environment — это название виртуального окружения. может быть любым

# активация виртуального окружениея
source my_new_environment/bin/activate
# выход из виртуального окружениея
deactivate

# посмотреть список пакетов 
pip list --format=json
```

#### Cоздание пакетов 
```
hello-world
├── hello_world
│   ├── __init__.py
│   └── main.py
└── README
└── setup.py
1 directory, 2 files
```
#### Нативные пакеты Python

нативные утилиты создания пакетов Python и средства их размещения (PyPI)
создадим новую виртуальную среду и активируем ее:

```
mkdir /tmp/packaging
cd /tmp/packaging
python3 -m venv /tmp/packaging
source /tmp/packaging/bin/activate

# setuptools — набор утилит для создания пакетов;
# twine — утилита для регистрации пакетов и загрузки их на сервер.

pip install setuptools twine

# создаем структуру проекта
hello-world
├── hello_world
│   ├── __init__.py
│   └── main.py
└── README
└── setup.py

# Для генерации нативного пакета Python необходимо добавить в проект 

cat setup.py
# -----
from setuptools import setup, find_packages
setup(
    name="hello-world",
    version="0.0.1",
    author="Example Author",
    author_email="stopspamer@ukr.net",
    url="example.com",
    description="A hello-world example package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# -----

# Для генерации на его основе дистрибутива исходного кода выполните следующую команду:
python3 setup.py sdist

# В каталоге верхнего уровня проекта появился новый каталог dist, он содержит 
# дистрибутив исходного кода — файл hello-world-0.0.1.tar.gz - его можно установить
pip install dist/hello-world-0.0.1.tar.gz 

# Структура каталога
hello-world
├── dist
│   └── hello-world-0.0.1.tar.gz
├── hello_world
│   ├── __init__.py
│   └── main.py
├── hello_world.egg-info
│   ├── dependency_links.txt
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   └── top_level.txt
├── README
└── setup.py



# Python (PyPI) — это репозиторий программного обеспечения на языке Python

# Загрузить пакет в репозиторий нужны креды 
twine upload --repository  dist/hello-world-0.0.1.tar.gz

# После загрузки можно проверить, появился ли пакет на PyPI. Для этого перейдите по ссылке https://pypi.org/project/<имя_пакета>

# установить из репозитория
python3 -m pip install --index-url https://test.pypi.org/simple/ hello-world
Enter your password:



# Сборка пакета для DEB RPM см книгу Стр 166