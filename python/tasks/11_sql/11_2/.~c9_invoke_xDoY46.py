# -*- coding: utf-8 -*-

'''
скрипт принимает аргументы и в соответсвии с ними выводит информацию из базы данных
* key - имя столбца, по которому надо найти информацию
* value - значение
-------
* если скрипт был вызван без аргументов, вывести всё содержимое таблицы dhcp
 * отформатировать вывод в виде столбцов
* если скрипт был вызван с двумя аргументами, вывести информацию из таблицы dhcp, которая соответствует полю и значению
 * провести проверку на корректность аргументов
* если скрипт был вызван с любым другим количеством аргументов, вывести сообщение, что скрипт поддерживает только два или ноль аргументов
'''
from pprint import pprint
import sqlite3
import sys


db_filename = 'dhcp_snooping.db'

##################################

def Print_Full_Table():
    conn = sqlite3.connect(db_filename)       
    query = 'SELECT * from dhcp'  
    result = conn.execute(query)
    print('-' * 80)
    for row in result:
       print ('%-20s'%row[0],'%-15s'%row[1],'%-5s'%row[2],'%-25s'%row[3],'%-5s'%row[4])  
    return
#######################################
def Control_argument (key, value):
    """ Проверка аргументов и вывод информации по значению"""
    if not key in keys:
        print('Enter key from {}'.format(', '.join(keys)))
        
    elif:
        
    elif

    
    
    Print_Table (key,value)
    return
########################################
def Print_Table (key,value):
    """ Вывод таблицы по ключу и значению"""
    conn = sqlite3.connect(db_filename)       
    conn.row_factory = sqlite3.Row                                # позволяет далее обращаться к данным в колонках по имени колонки
    
    keys.remove(key)                                              # удаления ключа из списка (он не будет в выдаче)
    print('\nDetailed information for host(s) with', key, value)
    print('-' * 40)
    """
    из БД выбираются те строки, в которых ключ равен указанному значению
    в SQL значения можно подставлять через знак вопроса, но нельзя
    подставлять имя столбца. Поэтому имя столбца подставляется через
    форматирование строк, а значение - штатным средством SQL.
    Обратите внимание на (value,) - таким образом передается кортеж с одним элементом
    """
    query = 'select * from dhcp where {} = ?'.format( key )       
    result = conn.execute(query, (value,))
    
    for row in result:
        for k in keys:
            print('{:12}: {}'.format(k, row[k]))
    print('-' * 40)
    
    

###############MAIN###############
if __name__ == "__main__":
    # ВХОДНЫЕ ДАННЫЕ
    #key, value, other = sys.argv[1:]                               # чтение аргументво из скрипта
    #key, value = 'ip', '10.1.10.2'
    #key, value = 'vlan', '10'
    # Проверка на контроль количества аргументов
    key, value = '',''
    #key, value = '', '22'
    #key, value = 'vlan', '10','x'
    # Проверка на корректность входных параметров
    #key, value = 'vlant', '10'
    #key, value = 'vlant', '00:09:-:3D:D6:58'
    #key, value = 'vlan', '10.1.10.2a'
    #key, value = 'vlan', '10.1.10.2234'
    #key, value = 'vlan', 'Fastedrvs23rnet0/1'
    #key, value = 'vlan', '#sw1'
   
    print ('key   ', type(key), key)
    print ('value ', type(value), value)
    
    keys = ['mac', 'ip', 'vlan', 'interface', 'switch']     # список ключей       
    
    if not key and not value: #and argv[2]:   # кусок используется для передачи параметров ручками
        print ('вывод полной таблицы')
        Print_Full_Table()
    elif key and value:# and not other:
        print ('Аргументов два')
        Control_argument (key, value)
    else:
        print ('Cкрипт поддерживает только два или ноль аргументов')
            