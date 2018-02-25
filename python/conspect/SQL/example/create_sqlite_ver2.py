import sqlite3
import re
# 00:09:BB:3D:D6:58  10.1.10.2        86250     dhcp-snooping 10   FastEthernet0/1
regex = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')

result = []

with open('dhcp_snooping.txt') as data:
    for line in data:
        match = regex.search(line)
        if match:
            result.append(match.groups())
print ('Parsing dhcp_snooping.txt ')
print (result)
conn = sqlite3.connect('dhcp_snooping.db')

print('Creating schema...')
with open('dhcp_snooping_schema.sql', 'r') as f:
    schema = f.read()
    conn.executescript(schema)
print('Done')

print('Inserting DHCP Snooping data')

for row in result:
    try:
        with conn:
            query = '''insert into dhcp (mac, ip, vlan, interface)
                       values (?, ?, ?, ?)'''
            conn.execute(query, row)
    except sqlite3.IntegrityError as e:
        print('Error occured: ', e)

conn.close()
"""
в регулярном выражении, которое проходится по выводу команды sh ip dhcp snooping binding, 
используются не именованные группы, как в примере раздела 
Регулярные выражения, а нумерованные
группы созданы только для тех элементов, которые нас интересуют
result - это список, в котором хранится результат обработки вывода команды
но теперь тут не словари, а кортежи с результатами
это нужно для того, чтобы их можно было сразу передавать на запись в БД

Перебираем в полученном списке кортежей элементы
В этом скрипте используется еще один вариант записи в БД
строка query описывает запрос. Но вместо значений указываются знаки
вопроса. Такой вариант записи запроса позволяет динамически подставлять значение полей
затем методу execute передается строка запроса и кортеж row, где находятся значения


$ python create_sqlite_ver2.py
Creating schema...
Done
Inserting DHCP Snooping data

"""

"""
Проверим, что данные записались:
$ sqlite3 dhcp_snooping.db "select * from dhcp"
-- Loading resources from /home/vagrant/.sqliterc
mac ip vlan interface
----------------- ---------- ---------- ---------------
00:09:BB:3D:D6:58 10.1.10.2 10 FastEthernet0/1
00:04:A3:3E:5B:69 10.1.5.2 5 FastEthernet0/1
00:05:B3:7E:9B:60 10.1.5.4 5 FastEthernet0/9
00:09:BC:3F:A6:50 10.1.10.6 10 FastEthernet0/3



"""
# sqlite3 /home/ubuntu/workspace/python/conspect/SQL/example/dhcp_snooping.db "select * from dhcp"










