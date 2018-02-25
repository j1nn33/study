import sqlite3

conn = sqlite3.connect('dhcp_snooping.db')

print('Creating schema...')
with open('dhcp_snooping_schema.sql', 'r') as f:
    schema = f.read()
    conn.executescript(schema)
print("Done")

conn.close()

"""
при выполнении строки conn = sqlite3.connect('dhcp_snooping.db') :
создается файл dhcp_snooping.db, если его нет создается объект Connection
в БД создается таблица (если ее не было) на основании команд, которые указаны
в файле dhcp_snooping_schema.sql:
открывается файл dhcp_snooping_schema.sql
schema = f.read() - весь файл считывается в одну строку
conn.executescript(schema) - метод executescript позволяет выполнять
команды SQL, которые прописаны в файле

Выполнение скрипта:
$ python create_sqlite_ver1.py
Creating schema...
Done
"""
# В результате должен быть создан файл БД и таблица dhcp.
# Проверить, что таблица создалась, можно с помощью утилиты sqlite3, которая
# позволяет выполнять запросы прямо в командной строке.
# Список созданных таблиц выводится таким образом:
# $ sqlite3 dhcp_snooping.db "SELECT name FROM sqlite_master WHERE type='table'"
# dhcp
# 
# sqlite3 /home/ubuntu/workspace/python/conspect/SQL/example/dhcp_snooping.db "SELECT name FROM sqlite_master WHERE type='table'"