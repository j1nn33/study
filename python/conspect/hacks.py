# в Python объект считается false, только если он пуст. 
my_object = 'Test' # True example
my_object = ''     # False example

#  Проверка на вхождение подстроки

string = 'Hi there' # True example
if 'Hi' in string:
    print 'Success!'

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


