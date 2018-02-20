import sqlite3

# Объект Connection - это подключение к конкретной БД. Можно сказать, что этот объект представляет БД.
connection = sqlite3.connect('dhcp_snooping.db')        # создается база hcp_snooping.db в папке с кодом программы

# Создается курсор из соединения с БД
cursor = connection.cursor() 

# Выполнение команд SQL

execute()       - метод для выполнения одного выражения SQL
executemany()   - метод позволяет выполнить одно выражение SQL для последовательности параметров (или для итератора)
executescript() - метод позволяет выполнить несколько выражений SQL за один раз


# Метод execute позволяет выполнить одну команду SQL.

print (cursor.execute("create table switch (mac text not NULL primary key, hostname text, model text, location text)"))

# <sqlite3.Cursor at 0x1085be880>

# Выражения SQL могут быть параметризированы - вместо данных можно подставлять
# специальные значения. За счет этого можно использовать одну и ту же команду SQL
# для передачи разных данных.

data = [
('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]

query = "INSERT into switch values (?, ?, ?, ?)"
 
#Знаки вопроса в команде используются для подстановки данных, которые будут
#передаваться методу execute.
# Теперь можно передать данные таким образом:
for row in data:
    cursor.execute(query, row)
    
    
# Второй аргумент, который передается методу execute, должен быть кортежем. Если
# нужно передать кортеж с одним элементом, используется запись (value, ) .
# Чтобы изменения были применены, нужно выполнить commit (обратите внимание, что
# метод commit вызывается у соединения):
connection.commit()
# Теперь, при запросе из командной строки sqlite3, можно увидеть эти строки в таблице  switch:

# см sqlite 1

"""  executemany - позволяет выполнить одну команду SQL для последовательности параметров (или для итератора)."""
# С помощью метода executemany в таблицу switch можно добавить аналогичный список данных одной командой

data2 = [
('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str'),
('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str'),
('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str'),
('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')]
query = "INSERT into switch values (?, ?, ?, ?)"
cursor.executemany(query, data2)
connection.commit()

""" executescript - позволяет выполнить несколько выражений SQL за один раз."""
# Особенно удобно использовать этот метод при создании таблиц
connection = sqlite3.connect('new_db.db')
cursor = connection.cursor()
cursor.executescript('''
                        create table switches(
                            hostname text not NULL primary key,
                            location text
                        );

                        create table dhcp(
                            mac text not NULL primary key,
                            ip text,
                            vlan text,
                            interface text,
                            switch text not null references switches(hostname)
                        );
                        ''')
                        
-------------------------------------------------------------                        
Получение результатов запроса

- использование методов fetch...() - в зависимости от метода возвращаются одна, несколько или все строки
- использование курсора как итератора - возвращается итератор

""" fetchone - возвращает одну строку данных"""
import sqlite3
connection = sqlite3.connect('sw_inventory.db')
cursor = connection.cursor()
cursor.execute('select * from switch')
# <sqlite3.Cursor at 0x104eda810>
cursor.fetchone()
# ('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')

# хотя запрос SQL подразумевает, что запрашивалось всё
#содержимое таблицы, метод fetchone вернул только одну строку.
#Если повторно вызвать метод, он вернет следующую строку:
print(cursor.fetchone())
#('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str')

#Аналогичным образом метод будет возвращать следующие строки. После обработки
#всех строк метод начинает возвращать None.
#За счет этого метод можно использовать в цикле, например, так:
cursor.execute('select * from switch')
#<sqlite3.Cursor at 0x104eda810>
while True:
    next_row = cursor.fetchone()
    if next_row:
        print(next_row)
    else:
        break

#('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')
#('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str')


"""fetchmany возвращает список строк данных."""
cursor.fetchmany([size=cursor.arraysize])
# С помощью параметра size можно указывать, какое количество строк возвращается.
# По умолчанию параметр size равен значению cursor.arraysize:
print(cursor.arraysize)
# 1
Например, таким образом можно возвращать по три строки из запроса:
    
cursor.execute('select * from switch')
# <sqlite3.Cursor at 0x104eda810>
from pprint import pprint
while True:
three_rows = cursor.fetchmany(3)
if three_rows:
    pprint(three_rows)
else:
    break
# [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
#  ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
#  ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str')]
# [('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str'),
#  ('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str'),
#  ('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str')]
# [('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str'),
#  ('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')]

""" fetchall возвращает все строки в виде списка"""
cursor.execute('select * from switch')
cursor.fetchall()
#[('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
# ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
# ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
# ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str'),
# ('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str'),
# ('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str'),
# ('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str'),
# ('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')]

Важный аспект работы метода - он возвращает все оставшиеся строки.
То есть, если до метода fetchall использовался, например, метод fetchone, то метод
fetchall вернет оставшиеся строки запроса
------------------------------------------------
""" Cursor как итератор"""
Если нужно построчно обрабатывать результирующие строки, лучше использовать
курсор как итератор. При этом не нужно использовать методы fetch.
При использовании методов execute возвращается курсор. А, так как курсор можно
использовать как итератор, можно использовать его, например, в цикле for:


result = cursor.execute('select * from switch')
for row in result:
    print(row)
# ('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')
# ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str')


И, конечно же, аналогичный вариант отработает и без присваивания переменной:
for row in cursor.execute('select * from switch'):
    print(row)
# ('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')
# ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str')
# ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str')

----------------------------------------------------
Использование модуля sqlite3 без явного создания курсора

Методы execute доступны и в объекте Connection, и в объекте Cursor.
 А методы fetch доступны только в объекте Cursor.
При использовании методов execute с объектом Connection курсор возвращается как
результат выполнения метода execute. Его можно использовать как итератор и
получать данные без методов fetch.
За счет этого при работе с модулем sqlite3 можно не создавать курсор.
Пример итогового скрипта (файл create_sw_inventory_ver1.py)


-----------------------------------------
"""Обработка исключений"""
пример использования метода execute при возникновении ошибки.
В таблице switch поле mac должно быть уникальным. И, если попытаться записать
пересекающийся MAC-адрес, возникнет ошибка:

con = sqlite3.connect('sw_inventory2.db')
query = "INSERT into switch values ('0000.AAAA.DDDD', 'sw7', 'Cisco 2960', 'London, Green Str')"
con.execute(query)

# IntegrityError Traceback (most recent call last)
# <ipython-input-56-ad34d83a8a84> in <module>()
# ----> 1 con.execute(query)
# IntegrityError: UNIQUE constraint failed: switch.mac

Соответственно, можно перехватить исключение:
try:
    con.execute(query)
except sqlite3.IntegrityError as e:
    print("Error occured: ", e)

# Error occured: UNIQUE constraint failed: switch.mac

Обратите внимание, что надо перехватывать исключение sqlite3.IntegrityError, а не IntegrityError
см пример create_sw_inventory_ver2.py
----------------------------------------------------------

"""Connection как менеджер контекста"""

После выполнения операций изменения должны быть сохранены (надо выполнить commit() ), 
а затем можно закрыть соединение, если оно больше не нужно.
Python позволяет использовать объект Connection как менеджер контекста. В таком
случае, не нужно явно делать commit. 

При этом:
    при возникновении исключения, транзакция автоматически откатывается
    если исключения не было, автоматически выполняется commit
    Пример использования соединения с базой как менеджера контекстов (create_sw_inventory_ver2.py):
    Обратите внимание, что хотя транзакция будет откатываться при возникновении
    исключения, само исключение всё равно надо перехватывать.
    
"""Проверка на Коллизию """

Для проверки этого функционала надо записать в таблицу данные, в которых MAC-
адрес повторяется. Но прежде, чтобы не повторять части кода, лучше разнести код в
файле create_sw_inventory_ver2.py по функциям (файл create_sw_inventory_ver2_functions.py)

Проверка содержимого БД
[('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
 ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
 ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]


Теперь проверим, как функция write_data_to_db отработает при наличии одинаковых
MAC-адресов в данных.
Connection как менеджер контекста

В файле create_sw_inventory_ver3.py используются функции из файла
create_sw_inventory_ver2_functions.py и подразумевается, что скрипт будет запускаться
после записи предыдущих данных:
    
Проверка текущего содержимого БД
[('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
 ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
 ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]
------------------------------------------------------------
Попытка записать данные с повторяющимся MAC-адресом:
[('0055.AAAA.CCCC', 'sw5', 'Cisco 3750', 'London, Green Str'),
 ('0066.BBBB.CCCC', 'sw6', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw7', 'Cisco 2960', 'London, Green Str'),
 ('0088.AAAA.CCCC', 'sw8', 'Cisco 3750', 'London, Green Str')]
Error occured:  UNIQUE constraint failed: switch.mac

Проверка содержимого БД
[('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
 ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
 ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
 ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]

___________________________________________________________