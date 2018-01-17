# в Python объект считается false, только если он пуст. 
my_object = 'Test' # True example
my_object = ''     # False example

#  Проверка на вхождение подстроки

string = 'Hi there' # True example
if 'Hi' in string:
    print ('Success!')

# enumerate

list_a = ['a','b','c']
for counter, value in enumerate(list_a):
    print(counter, value)


# Лямбда-функции
# Следующие два определения полностью идентичны:
def add(a,b): return a+b

add2 = lambda a,b: a+b
"""
Синтаксис лямбда-функции: lambda переменные: выражение
переменные — список аргументов, разделенных запятой. Нельзя использовать ключевые слова. Аргументы не надо заключать в скобки.
выражение — инлайновое выражение Python. Область видимости включает локальные переменные и аргументы. Функция возвращает результат этого выражения.
"""

# Списки
numbers = [1,2,3,4,5]
squares = map(lambda x: x*x, numbers)

# или
numbers = [1,2,3,4,5]
squares = [number*number for number in numbers]

# squares = [1,4,9,16,25]

numbers = [1,2,3,4,5]
numbers_under_4 = filter(lambda x: x < 4, numbers)

# numbers_under_4 = [1,2,3]

# списки
# убедиться, что элементы списка уникальны. преобразовать его в сет и проверить, изменилась ли длина
numbers = [1,2,3,3,4,1]
set(numbers)
# возвращает set([1,2,3,4])
 
if len(numbers) == len(set(numbers)):
    print ('List is unique!')
# не выводит ничего 

# словари

# создание
dict(a=1, b=2, c=3)
# возвращает {'a': 1, 'b': 2, 'c': 3} 

# преобразование словаря в список

dictionary = {'a': 1, 'b': 2, 'c': 3}
dict_as_list = dictionary.items()

#dict_as_list = [('a', 1), ('b', 2), ('c', 3)] 

# Преобразование списка в словарь

dict_as_list = [['a', 1], ['b', 2], ['c', 3]]
dictionary = dict(dict_as_list)
# dictionary = {'a': 1, 'b': 2, 'c': 3} 


dict_as_list = [['a', 1], ['b', 2], ['c', 3]]
dictionary = dict(dict_as_list, d=4, e=5)
# dictionary = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5} 


# Функции

# Значения по умолчанию для аргументов вычисляются только один раз

def function(item, stuff = []):
    stuff.append(item)
    print (stuff)

function(1)
# выводит '[1]'

function(2)
# выводит '[1,2]' !!!
"""
Значения по умолчанию для аргументов вычисляются только один раз, в момент определения функции. Python просто присваивает это значение нужной переменной при каждом вызове функции. При этом он не проверяет, изменилось ли это значение. Поэтому, если вы изменили его, изменение будет в силе при следующих вызовах функции. В предыдущем примере, когда мы добавили значение к списку stuff, мы изменили его значение по умолчанию навсегда. Когда мы вызываем функцию снова, ожидая дефолтное значение, мы получаем измененное. 
"""
def function(item, stuff = None):
    if stuff is None:
        stuff = []
    stuff.append(item)
    print (stuff)

function(1)
# выводит '[1]'

function(2)
# выводит '[2]', как и ожидалось

########################################################
# Заставляем дефолтные значения вычисляться каждый раз

#Если вы не хотите вносить в код функции лишний беспорядок, можно заставить интерпретатор заново вычислять #значения аргументов перед каждым вызовом. Следующий декоратор делает это:
from copy import deepcopy

def resetDefaults(f):
    defaults = f.func_defaults
    def resetter(*args, **kwds):
        f.func_defaults = deepcopy(defaults)
        return f(*args, **kwds)
    resetter.__name__ = f.__name__
    return resetter

#Просто примените этот декоратор к функции, чтобы получить ожидаемые результаты:
@resetDefaults # так мы применяем декоратор
def function(item, stuff = []):
    stuff.append(item)
    print (stuff)

function(1)
# выводит '[1]'

function(2)
# выводит '[2]', как и ожидалось
########################################################
# Декораторы
# Декоратор — это функция, оборачивающая другую функцию: сначала создается 
# главная функция, затем она  передается декоратору. Декоратор возвращает 
# новую функцию, которая используется вместо первоначальной в остальной части программы

def decorator1(func):
    return lambda: func() + 1
 
def decorator2(func):
    def print_func():
        print (func())
    return (print_func)
 
@decorator2
@decorator1
def function():
    return 41
 
function()
# печатает "42" 
"""
function передается в decorator1, а он возвращает функцию, 
которая вызывает function и возвращает число, большее ее 
результата на единицу. Эта функция передается в decorator2, 
который ее вызывает и печатает результат. 
"""

# Следующий пример делает абсолютно то же, но более многословно: 

def decorator1(func):
    return lambda: func() + 1
 
def decorator2(func):
    def print_func():
        print (func())
    return print_func
 
def function():
    return 41
 
function = decorator2(decorator1(function))
 
function()
# печатает "42" 

# Запуск одной из нескольких функций при помощи словаря

def key_1_pressed():
    print ('Нажата клавиша 1')
 
def key_2_pressed():
    print ('Нажата клавиша 2')
 
def key_3_pressed():
    print ('Нажата клавиша 3')
 
def unknown_key_pressed():
    print ('Нажата неизвестная клавиша')

keycode = 2
if keycode == 1:
   key_1_pressed()
elif keycode == 2:
   key_2_pressed()
elif number == 3:
   key_3_pressed()
else:
   unknown_key_pressed()
# выводит "Нажата клавиша 2

# или

keycode = 2
functions = {1: key_1_pressed, 2: key_2_pressed, 3: key_3_pressed}
functions.get(keycode, unknown_key_pressed)()

# Метод get() возвращает значение для данного ключа. 
# Если ключ не доступен, то возвращает значение по умолчанию 
# key - это ключ для поиска в словаре.
# по default - это значение , которое должно быть возвращено в случае 


# Классы

# Проверка на существование метода или свойства
class Class:
    answer = 42
 
hasattr(Class, 'answer')
# возвращает True
hasattr(Class, 'question')
# возвращает False 

class Class:
    answer = 42
 
getattr(Class, 'answer')
# возвращает 42
getattr(Class, 'question', 'Сколько будет 6x9?')
# возвращает "Сколько будет 6x9?"
getattr(Class, 'question')
# бросает исключение AttributeError 

# Если вы написали класс так, что необходимо проверять существование 
# свойств, то вы всё сделали неправильно. Свойство должно существовать 
# всегда, а если оно не используется, можно установить его в None. 

