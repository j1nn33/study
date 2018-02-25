import os
import sqlite3
import re

data_filename = 'dhcp_snooping.txt'
db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'

regex = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')

result = []

with open('dhcp_snooping.txt') as data:
    for line in data:
        match = regex.search(line)
        if match:
            result.append(match.groups())

db_exists = os.path.exists(db_filename)

conn = sqlite3.connect(db_filename)

if not db_exists:
    print('Creating schema...')
    with open(schema_filename, 'r') as f:
        schema = f.read()
    conn.executescript(schema)
    print('Done')
else:
    print('Database exists, assume dhcp table does, too.')

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
Теперь есть проверка наличия файла БД, и файл dhcp_snooping.db будет создаваться
только в том случае, если его нет. Данные также записываются только в том случае,
если не создан файл dhcp_snooping.db.
Разделение процесса создания таблицы и заполнения ее данными вынесено в
задания к разделу.

Пример использования SQLite
Если файла нет (предварительно его удалить):
$ rm dhcp_snooping.db
$ python create_sqlite_ver3.py
Creating schema...
Done
Inserting DHCP Snooping data


Проверим. В случае, если файл уже есть, но данные не записаны:
$ rm dhcp_snooping.db
$ python create_sqlite_ver1.py
Creating schema...
Done


$ python create_sqlite_ver3.py
Database exists, assume dhcp table does, too.
Inserting DHCP Snooping data

Если есть и БД и данные:
$ python create_sqlite_ver3.py
Database exists, assume dhcp table does, too.
Inserting DHCP Snooping data
Error occured: UNIQUE constraint failed: dhcp.mac
Error occured: UNIQUE constraint failed: dhcp.mac
Error occured: UNIQUE constraint failed: dhcp.mac
Error occured: UNIQUE constraint failed: dhcp.mac
"""