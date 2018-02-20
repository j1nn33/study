"""
        Коментарии
        Коментарии
        Коментарии
"""
string1 = 'ИСХОДНАЯ СТРОКА'
string1.find('подстрока')
результат номер позиции начала подстроки


"--------------ТИПЫ ДАННЫХ"
"""
    1. None (неопределенное значение переменной)
    2. Логические переменные ( Boolean Type )
    3. Числа ( Numeric Type )
        int – целое число
        float – число с плавающей точкой
        complex – комплексное число
    4. Списки ( Sequence Type )
        list – список
        tuple – кортеж
        range – диапазон
    5. Строки ( Text Sequence Type )
        str
    6. Бинарные списки ( Binary Sequence Types )
        bytes – байты
        bytearray – массивы байт
        memoryview – специальные объекты для доступа к внутренним данным
                    объекта через protocol buffer
    7. Множества ( Set Types )
        set – множество
        frozenset – неизменяемое множество
    8. Словари ( Mapping Types )
        dict – словарь
"""

"--------------КЛЮЧЕВЫЕ СЛОВА (зарезервированные системой)"
import keyword
print ("Python keywords: " , keyword.kwlist)
"Проверить является или нет идентификатор ключевым словом можно так:"
keyword.iskeyword( "try" )
"True"
keyword.iskeyword( "b" )
"False"
"--------------INPUT - OUTPUT"

number = int(input("ENTER A NUMBER: "))
print("THE NUMBER IS", (number))

print ( "Age: " + str ( 23 ))
"Age: 23"

print ( "A" , "B" , "C" , sep= "#" )
"A#B#C"

tv = int ( input ( "input number: " ))
"input number: 334"
print (tv)
"334"

"""Преобразование строки в список осуществляется с помощью метода split(),
по умолчанию, в качестве разделителя, используется пробел."""
l = input ().split()
"1 2 3 4 5 6 7"
print (l)
"[ '1' , '2' , '3' , '4' , '5' , '6' , '7' ]"

"""Разделитель можно заменить, указав его в качестве 
аргумента метода split() ."""
nl = input ().split( "-" )
"1-2-3-4-5-6-7"
print (nl)
"[ '1' , '2' , '3' , '4' , '5' , '6' , '7' ]"

"""Для считывания списка чисел с одновременным приведением
их к типу int можно воспользоваться вот такой конструкцией."""
nums = map ( int , input().split())
"1 2 3 4 5 6 7"
print ( list (nums))
"[1, 2, 3, 4, 5, 6, 7]"

############################################################
access_template = ['switchport mode access',
'switchport access vlan {}',
'switchport nonegotiate',
'spanning-tree portfast',
'spanning-tree bpduguard enable']
print('\n'.join(access_template).format(5))

"""
Сначала элементы списка объединяются в строку, которая разделена символом \n , а
в строку подставляется номер VLAN, используя форматирование строк.


switchport mode access
switchport access vlan 5
switchport nonegotiate
spanning-tree portfast
spanning-tree bpduguard enable
"""
#######################################################
"--------------Условные операторы и циклы"
a = int ( input ( "введите число:" ))

if a < 0 :
    print ( "Neg" )
elif a == 0 :
    print ( "Zero" )
else:
    print ( "Pos" )

a = 0
while a >= 0 :
    if a == 7 :
        break
    a += 1
    print ( "A" )


a = - 1
while a < 10 :
    a += 1
    if a >= 7 :
        continue
    print ( "A" )
"""При запуске данного кода символ “А ” будет напечатан 7 раз, 
несмотря на то, что всего будет выполнено 11 проходов цикла."""

lst = [ 1 , 3 , 5 , 7 , 9 ]
for i in lst:
    print (i ** 2 )

word_str = "Hello, world!"
for l in word_str:
    print (l)
"""Строка “ Hello, world! ” будет напечатана в столбик."""



"--------------FUNCTION & FOR "
def print_number(limit):
    """my doc  - documetation of this function
    """
    for i in range(limit):
        print("i",i)

print_number(n)

def summa(a, b):
    return a + b

summa( 3 , 4 )

"--------------СПИСКИ"
"списки a = [ 1 , 3 , 5 , 7 ] изменяемые кортежи  b = ( 1 , 2 , 3 ) нет " \
"Доступ к элементам кортежа осуществляется также как к элементам списка"
" – черезуказание индекса."
int_list = [1, 2, 3, 4]
char_list = ['a', 'c', 'z']
empty_list = []
print("digit list", int_list)
"обращение к элементам списка через индексы"
my_list = [5, 7, 8, 2, 14]
print(my_list[1])
print(my_list[-1])
"вывод последнего элемена"
index = int(input("enter index of element"))
element = my_list[index]
print(element)

""""создать копию списка """
a = [ 1 , 3 , 5 , 7 ]
b = a[:]
c = list (a)

"""v - ссылка на список а не копия """
v = a

"""добавление и удаление элементов"""
a = []
a.append( 3 )
a.append( "hello" )
print (a)
а.remove( 3 )
del а[ 2 ]
"""удаление элемента по индексу"""
"""Методы списков """


list.append(x)
Добавляет элемент в конец списка. Ту же операцию можно сделать так a[len(a):] =
[x] .
>>> a = [ 1 , 2 ]
>>> a.append( 3 )
>>> print (a)
[ 1 , 2 , 3 ]


list.extend(L)
Расширяет существующий список за счет добавления всех элементов из списка L.
Эквивалентно команде a[len(a):] = L .
>>> a = [ 1 , 2 ]
>>> b = [ 3 , 4 ]
>>> a.extend(b)
>>> print (a)
[ 1 , 2 , 3 , 4 ]


list.insert(i, x)
Вставить элемент x в позицию i . Первый аргумент – индекс элемента после
которого будет вставлен элемент x .
>>> a = [ 1 , 2 ]
>>> a.insert( 0 , 5 )
>>> print (a)
[ 5 , 1 , 2 ]
>>> a.insert( len (a), 9 )
>>> print (a)
[ 5 , 1 , 2 , 9 ]


list.remove(x)
Удаляет первое вхождение элемента x из списка.
>>> a = [ 1 , 2 , 3 ]
>>> a.remove( 1 )
>>> print (a)
[ 2 , 3 ]


list.pop([i])
Удаляет элемент из позиции i и возвращает его. Если использовать метод без
аргумента, то будет удален последний элемент из списка.
>>> a = [ 1 , 2 , 3 , 4 , 5 ]
>>> print (a.pop( 2 ))
3
>>> print (a.pop())
5
>>> print (a)
[ 1 , 2 , 4 ]


list.clear()
Удаляет все элементы из списка. Эквивалентно del a[:] .
>>> a = [ 1 , 2 , 3 , 4 , 5 ]
>>> print (a)
[ 1 , 2 , 3 , 4 , 5 ]
>>> a.clear()
>>> print (a)
[]


list.index(x[, start[, end]])
Возвращает индекс элемента.
>>> a = [ 1 , 2 , 3 , 4 , 5 ]
>>> a.index( 4 )
3

list.count(x)
Возвращает количество вхождений элемента x в список.
>>> a = [ 1 , 2 , 2 , 3 , 3 ]
>>> print (a.count( 2 ))
2

list.sort(key=None, reverse=False)
Сортирует элементы в списке по возрастанию. Для сортировки в обратном порядке
используйте флаг reverse=True. Дополнительные возможности открывает параметр
key , за более подробной информацией обратитесь к документации.
>>> a = [ 1 , 4 , 2 , 8 , 1 ]
>>> a.sort()
>>> print (a)
[ 1 , 1 , 2 , 4 , 8 ]

list.reverse()
Изменяет порядок расположения элементов в списке на обратный.
>>> a = [ 1 , 3 , 5 , 7 ]
>>> a.reverse()
>>> print (a)
[ 7 , 5 , 3 , 1 ]

list.copy()
Возвращает копию списка. Эквивалентно a[:] .
>>> a = [ 1 , 7 , 9 ]
>>> b = a.copy()
>>> print (a)
[ 1 , 7 , 9 ]
>>> print (b)
[ 1 , 7 , 9 ]
>>> b[ 0 ] = 8
>>> print (a)
[ 1 , 7 , 9 ]
>>> print (b)
[ 8 , 7 , 9 ]

"""
"-------------СЛОВАРИ"
"Данные в словаре хранятся в формате ключ – значение"
 d1 = dict ( Ivan = "manager" , Mark = "worker" )
  print (d1)

"{ 'Mark' : 'worker' , 'Ivan' : 'manager' }"

"добавление элемента"
d1[ "China" ] = "Beijing"

"Удаление элемента через ключ"
del d1[ " Ivan" ]
"""


"-------------КЛАССЫ и ОБЪЕКТЫ"
"создание класса MyObject"
class MyObject:
    int_field = 8
    str_field = "a string"
    pass
"обращение к атрибутам класса"
print(MyObject.int_field)

"создание объекта из класса MyObject"
object = MyObject
"получение доступа к атрибутам класса через созданый объект"
print(object.int_field)

"Пример"

class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self._sex = uni "_ или __ это private atribute "
    def print_info(self):
        print(self.name, "is", self.age)

john = Person()
john.name = "John"
john.age = 22

lucy = Person("Lucy", 21)

john.print_info()
Person.print_info(john)
print(john.name, "is", john.age)



