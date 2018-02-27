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
import re
import ipaddress


db_filename = 'dhcp_snooping.db'

##################################
def Control_Value(value):
 
    # щаблоны регулярных выражений 
    regex_mac = re.compile('\w\w\:\w\w\:\w\w\:\w\w\:\w\w\:\w\w')
    regex_swich = re.compile('\w+')
    regex_eth = re.compile('\d+\/\d+')
    a=False                                                     # флаг по умолчанию value не корректно
    try:
        print ('1 -control ')
        ip = ipaddress.ip_address(value)                        # проверка на корректность ip adress
        a=True
        #print (ip)
    except ValueError:
        try:                                                    # проверка на корректность FastEthernet0/5
           print ('2 -control ')
           value.startswith('FastEthernet')                     # начало строки равно FastEthernet
           match_eth = regex_eth.search(value).group()          
           value.endswith(match_eth)                            # конец строки на соответвие шаблону
           if ('FastEthernet'+(regex_eth.search(value).group())) == value:    # проверка на соответсвие исходной строк, тк шаблон может быть жадным
               a=True
               print ('eth')
        except AttributeError:
            try:                                                # проверка на корректность mac
                print ('3 -control ')
                match_mac = regex_mac.fullmatch(value)          
                if match_mac:
                    a=True
                    print('mac')
                else:
                    try:                                        # проверка на корректность vlan
                        print ('4 -control ')
                        value = int(value)                      # преобразуем занчение к числу и если нет исключения то сравниваем значение
                        if value>=1 and value<=4096:
                            a=True
                        else:
                            print('vlan')
                    except ValueError:  
                        pass
                
                if a == False:
                    try:                                        # проверка на корректность vlan
                        print ('5 -control ')
                        match_sw = regex_swich.fullmatch(value)
                        if match_sw:
                            a=True
                        print('name')
                    except ValueError:
                        pass
            except AttributeError:
                pass
    
    
    return a
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
    
    #print (Control_Value (value))
    """ Проверка аргументов и вывод информации по значению"""
    if not key  in keys:
        print('ERROR --  Enter key from {}'.format(', '.join(keys)))
    elif not Control_Value(value):
        print('ERROR --  Value is not correct')
    else:
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
    #key, value = '',''
    #key, value = '', '22'
    #key, value = 'vlan', '10','x'
    # Проверка на корректность входных параметров (key)
    #key, value = 'vlant', '10'
    # Проверка на корректность входных параметров (value)
    key, value = 'vlan', '00:09:-:3D:D6:58'
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
            