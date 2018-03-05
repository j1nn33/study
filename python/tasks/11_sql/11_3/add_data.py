# -*- coding: utf-8 -*-

'''
Задание 11.3

add_data.py
* с помощью этого скрипта, выполняется добавление данных в БД
* добавлять надо не только данные из вывода sh ip dhcp snooping binding, но и информацию о коммутаторах

* вывод с трёх коммутаторов:
  * файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt

Поле active должно принимать такие значения:
 * 0 - означает False. И используется для того, чтобы отметить запись как неактивную
 * 1 - True. Используется чтобы указать, что запись активна

Каждый раз, когда информация из файлов с выводом DHCP snooping добавляется заново,
надо пометить все существующие записи (для данного коммутатора), как неактивные (active = 0).
Затем можно обновлять информацию и пометить новые записи, как активные (active = 1).

Таким образом, в БД останутся и старые записи, для MAC-адресов, которые сейчас не активны,
и появится обновленная информация для активных адресов.
'''
import os
import sqlite3
import re
import glob
#import yaml
import pprint

db_filename = 'dhcp_snooping.db'
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')
              # glob.glob(pathname) возвращение список соответствующих шаблону pathname.
              #print(dhcp_snoop_files)         # ['sw2_dhcp_snooping.txt', 'sw1_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
def update_info(db_filename):
    conn = sqlite3.connect(db_filename)
    data = []
    old_data = []
    query = 'SELECT * from dhcp'  
    data = conn.execute(query)
    for row in data:
        row=list(row)
        row.insert(-1,0)     # замена active на 0
        row.pop()
        row=tuple(row)
        old_data.append(row) # заполняем промежуточный список
    for row in old_data:
        try:
            with conn:
                query1 = '''REPLACE INTO dhcp (mac, ip, vlan, interface, switch, active)
                            values (?, ?, ?, ?, ?, ?)'''
                conn.execute(query1, row)
                print ('replace',row)
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
        row.append(1)
        row=tuple(row)
        print (row)
        
        try:
            with conn:
                query = '''REPLACE INTO dhcp (mac, ip, vlan, interface, switch, active)
                           values (?, ?, ?, ?, ?, ?)'''
                conn.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('Error occured: ', e)
    conn.close()
         
    return

######################################################
if __name__ == "__main__":
    # проверка на существование базы 
    db_exists = os.path.exists(db_filename)
    old_data=[]
    if not db_exists:
        print('Базы даных нет ее необходимо создать')
    else:
        print ('База существует')
        print('Getting & updating information from data base')
        update_info(db_filename)
        # добавление иформации из файлов dhcp_snoop_file реализованно в цикле 
        if dhcp_snoop_files:
            for dhcp_file in dhcp_snoop_files:
                ins_dhcp(dhcp_file)
        else:
            print ('file is not exist')
        
##################################################################################        
    """
    $ sqlite3 /home/ubuntu/workspace/python/tasks/11_sql/11_1/dhcp_snooping.db
    
    sqlite>SELECT name FROM sqlite_master WHERE type='table';
    switches
    dhcp
    
    dhcp
    sqlite>select * from dhcp;
    00:A9:BB:3D:D6:58|10.1.10.20|10|FastEthernet0/7|sw2|1
    00:B4:A3:3E:5B:69|10.1.5.20|5|FastEthernet0/5|sw2|1
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