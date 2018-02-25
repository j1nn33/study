# -*- coding: utf-8 -*-
import sqlite3
import sys

db_filename = 'dhcp_snooping.db'


#key, value = sys.argv[1:]
#key, value = 'ip', '10.1.10.2'
key, value = 'vlan', '10'



keys = ['mac', 'ip', 'vlan', 'interface']
keys.remove(key)

conn = sqlite3.connect(db_filename)

#Позволяет далее обращаться к данным в колонках, по имени колонки
conn.row_factory = sqlite3.Row

print('\nDetailed information for host(s) with', key, value)
print('-' * 40)

query = 'select * from dhcp where {} = ?'.format( key )
result = conn.execute(query, (value,))

for row in result:
    for k in keys:
        print('{:12}: {}'.format(k, row[k]))
    print('-' * 40)

"""
из аргументов, которые передали скрипту, считываются параметры key, value
из списка keys удаляется выбранный ключ. Таким образом, в списке остаются
только те параметры, которые нужно вывести подключаемся к БД
conn.row_factory = sqlite3.Row - позволяет далее обращаться к данным в
колонках по имени колонки
из БД выбираются те строки, в которых ключ равен указанному значению
в SQL значения можно подставлять через знак вопроса, но нельзя
подставлять имя столбца. Поэтому имя столбца подставляется через
форматирование строк, а значение - штатным средством SQL.
Обратите внимание на (value,) - таким образом передается кортеж с одним элементом
Полученная информация выводится на стандартный поток вывода:
перебираем полученные результаты и выводим только те поля, названия
которых находятся в списке keys


Проверим работу скрипта.


Показать параметры хоста с IP 10.1.10.2:
$ python /home/ubuntu/workspace/python/conspect/SQL/example/get_data_ver1.py ip 10.1.10.2
$ python get_data_ver1.py ip 10.1.10.2
Detailed information for host(s) with ip 10.1.10.2
----------------------------------------
mac : 00:09:BB:3D:D6:58
vlan : 10
interface : FastEthernet0/1
----------------------------------------
Показать хосты в VLAN 10:
$ python get_data_ver1.py vlan 10
Detailed information for host(s) with vlan 10
----------------------------------------
mac : 00:09:BB:3D:D6:58
ip : 10.1.10.2
interface : FastEthernet0/1
----------------------------------------
mac : 00:07:BC:3F:A6:50
ip : 10.1.10.6
interface : FastEthernet0/3
----------------------------------------

"""