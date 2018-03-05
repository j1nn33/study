# -*- coding: utf-8 -*-
"""
* сюда должна быть вынесена функциональность по созданию БД:
 * должна выполняться проверка наличия файла БД
 * если файла нет, согласно описанию схемы БД в файле dhcp_snooping_schema.sql,
   должна быть создана БД (БД отличается от примера в разделе)

В БД теперь две таблицы (схема описана в файле dhcp_snooping_schema.sql):
 * switches - в ней находятся данные о коммутаторах
 * dhcp - эта таблица осталась такой же как в примере, за исключением поля switch
  * это поле ссылается на поле hostname в таблице switches
"""
import os
import sqlite3

db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'

"""
      + плучение имени файла относительно каталогов
      - передача файла в базу данных
      - проверка на существование базы
      - создание базы
      - тестирование (вывод)
"""
def create_db (db_filename):
    db_exists = os.path.exists(db_filename)          
    conn = sqlite3.connect(db_filename)       
    
    if not db_exists:
        print('Creating schema...')
        with open(schema_filename, 'r') as f:
            schema = f.read()
        conn.executescript(schema)          # метод позволяет выполнить несколько выражений SQL за один раз
        print('Done')
    else:
        print('Database exists, assume dhcp table does, too.')
    
    conn.close()  
    return

if __name__ == "__main__":
    #print ('MAIN PROGRAMM')
    dir_db=os.getcwd()                                 # получение пути /home/ubuntu/workspace/python/tasks/11_sql/11_1
    db_filename=os.path.join(os.getcwd(),db_filename)  # /home/ubuntu/workspace/python/tasks/11_sql/11_1/dhcp_snooping.db
    #print (db_filename)
    create_db (db_filename)
    
# В результате должен быть создан файл БД и таблица dhcp.
# Проверить, что таблица создалась, можно с помощью утилиты sqlite3, которая
# позволяет выполнять запросы прямо в командной строке.
# Список созданных таблиц выводится таким образом:
# $ sqlite3 /home/ubuntu/workspace/python/tasks/11_sql/11_1/dhcp_snooping.db "SELECT name FROM sqlite_master WHERE type='table'"
# switches
# dhcp