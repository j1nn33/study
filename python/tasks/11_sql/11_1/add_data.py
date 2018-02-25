# -*- coding: utf-8 -*-

'''
Задание 11.1

add_data.py
* с помощью этого скрипта, выполняется добавление данных в БД
* добавлять надо не только данные из вывода sh ip dhcp snooping binding, но и информацию о коммутаторах


В файле add_data.py должны быть две части:
* информация о коммутаторах добавляется в таблицу switches
 * данные о коммутаторах, находятся в файле switches.yml
* информация на основании вывода sh ip dhcp snooping binding добавляется в таблицу dhcp
 * вывод с трёх коммутаторов:
   * файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
 * так как таблица dhcp изменилась, и в ней теперь присутствует поле switch, его нужно также заполнять. Имя коммутатора определяется по имени файла с данными

Код должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.
'''
import os
import sqlite3
import re
import glob
#import yaml
import pprint

db_filename = 'dhcp_snooping.db'
switches_yml= 'switches.yml'
#conn = sqlite3.connect(db_filename)
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')
              # glob.glob(pathname) возвращение список соответствующих шаблону pathname.
              #print(dhcp_snoop_files)         # ['sw2_dhcp_snooping.txt', 'sw1_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
def ins_switch(switches_yml):
    """добавление иформации из файла switches.yml"""
    with open(switches_yml) as f:
        templates = yaml.load(f)
    pprint.pprint(templates)

    print('PARSING YAML FILE ')
    result = []
    """
    {'switches': {'sw1': 'London, 21 New Globe Walk',
              'sw2': 'London, 21 New Globe Walk',
              'sw3': 'London, 21 New Globe Walk'}}
    методика обхода словаря
    1 цикл пробегаемся по первичным ключам 'switches'
        2 цикл пробегаемся по вториным ключам sw1, sw2, sw3
    """
    for key in templates.keys():
        for value in templates[key]:
            hostname = value
            location = templates[key][value]
            list_keys =tuple([hostname, location])
            result.append(list_keys)
    print(result)
    print('Inserting SWICHES DATA')
    conn = sqlite3.connect(db_filename)

    for row in result:
        try:
            with conn:
                query = '''insert into switches (hostname, location)
                           values (?, ?)'''
                conn.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('Error occured: ', e)
    conn.close()
    return


def ins_dhcp(dhcp_file):
    regex = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')
    regex_swich = re.compile('(\D+)+(\d+)')
    result = []
    
    with open (dhcp_file) as data:
        for line in data:
            match = regex.search(line)
            if match:
                result.append(match.groups())
    
    switch_name = match = regex_swich.search(dhcp_file).group()  # получение имени switch из имени файла
    
    print('Inserting DHCP Snooping data from file ', dhcp_file)
    conn = sqlite3.connect(db_filename)

    for row in result:
        # необходимо котреж преобразовать в список добавить switch_name и преобразовать обратно в котреж
        row=list(row)
        row.append(switch_name)
        row=tuple(row)
        print (row)
        try:
            with conn:
                query = '''insert into dhcp (mac, ip, vlan, interface, switch)
                           values (?, ?, ?, ?, ?)'''
                conn.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('Error occured: ', e)
    conn.close()
    return

######################################################
if __name__ == "__main__":
    # проверка на существование базы 
    db_exists = os.path.exists(db_filename)

    if not db_exists:
        print('Базы даных нет ее необходимо создать')
    else:
        print ('База существует')
        # добавление иформации из файла switches.yml
        if os.path.exists(switches_yml):
             print ('заполнение базы данных из switches_yml ')
             #ins_switch(switches_yml)
        else:
            print ('file switches.yml - не существует ') 
        
        # добавление иформации из файлов dhcp_snoop_file реализованно в цикле 
    
        if dhcp_snoop_files:
            for dhcp_file in dhcp_snoop_files:
                ins_dhcp(dhcp_file)
        else:
            print ('file is not exist')
    """
    проверка записей в таблице после вызова функции импорта из YAML
    $ sqlite3 /home/ubuntu/workspace/python/tasks/11_sql/11_1/dhcp_snooping.db
    
    sqlite>SELECT name FROM sqlite_master WHERE type='table';
    switches
    dhcp
    
    sqlite> select * from switches;
    sw1|London, 21 New Globe Walk
    sw2|London, 21 New Globe Walk
    sw3|London, 21 New Globe Walk
        
    dhcp
    sqlite>select * from dhcp;
    00:A9:BB:3D:D6:58|10.1.10.20|10|FastEthernet0/7|sw2
    00:B4:A3:3E:5B:69|10.1.5.20|5|FastEthernet0/5|sw2
    00:C5:B3:7E:9B:60|10.1.5.40|5|FastEthernet0/9|sw2
    00:A9:BC:3F:A6:50|10.1.10.60|20|FastEthernet0/2|sw2
    00:09:BB:3D:D6:58|10.1.10.2|10|FastEthernet0/1|sw1
    00:04:A3:3E:5B:69|10.1.5.2|5|FastEthernet0/10|sw1
    00:05:B3:7E:9B:60|10.1.5.4|5|FastEthernet0/9|sw1
    00:07:BC:3F:A6:50|10.1.10.6|10|FastEthernet0/3|sw1
    00:09:BC:3F:A6:50|192.168.100.100|1|FastEthernet0/7|sw1
    00:E9:BC:3F:A6:50|100.1.1.6|3|FastEthernet0/20|sw3
    
    sqlite> 
    """