import sqlite3
connection = sqlite3.connect('dhcp_snooping.db')
cursor = connection.cursor()
cursor.execute("create table switch (mac text not NULL primary key, hostname text, model text, location text)")
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
    
connection.commit()    # Чтобы изменения были применены, нужно выполнить commit

# все ниже набирается в коммандной строке

"""  
$ sqlite3 /python/conspect/SQL/dhcp_snooping.db
qlite> select * from switch;
mac            hostname   model      location
-------------- ---------- ---------- -----------------
0000.AAAA.CCCC sw1 Cisco 3750 London, Green Str
0000.BBBB.CCCC sw2 Cisco 3780 London, Green Str
0000.AAAA.DDDD sw3 Cisco 2960 London, Green Str
0011.AAAA.CCCC sw4 Cisco 3750 London, Green Str
"""