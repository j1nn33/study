
"""Connection как менеджер контекста

После выполнения операций изменения должны быть сохранены (надо выполнить commit() ), 
а затем можно закрыть соединение, если оно больше не нужно.
Python позволяет использовать объект Connection как менеджер контекста. В таком
случае, не нужно явно делать commit. 

При этом:
    при возникновении исключения, транзакция автоматически откатывается
    если исключения не было, автоматически выполняется commit
"""


# -*- coding: utf-8 -*-
import sqlite3

data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
        ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
        ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]

con = sqlite3.connect('sw_inventory3.db')
con.execute('''create table switch
               (mac text not NULL primary key, hostname text, model text, location text)''')

try:
    with con:
        query = 'INSERT into switch values (?, ?, ?, ?)'
        con.executemany(query, data)

except sqlite3.IntegrityError as e:
    print('Error occured: ', e)
    
# Обратите внимание, что хотя транзакция будет откатываться при возникновении
# исключения, само исключение всё равно надо перехватывать.

for row in con.execute('select * from switch'):
    print(row)

con.close()
