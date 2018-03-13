#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   + pds.create_db(args.name, args.schema)
   + pds.add_data_switches(args.db_file, args.filename)
   + pds.add_data(args.db_file, args.filename)
    pds.get_data(args.db_file, args.key, args.value)
    pds.get_all_data(args.db_file)
    
"""
import argparse
import os
import sqlite3
import re
import glob
#import yaml
import pprint
from pprint import pprint
import ipaddress

keys = ['mac', 'ip', 'vlan', 'interface', 'switch'] 
def create_db(db_filename, schema_filename):
    print ('db_filename ', db_filename)
    print ('schema_filename', schema_filename)
    print ('Create_db...')
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

def add_data_switches(db_filename, switches_yml):
    """добавление иформации из файла switches.yml"""
    with open(switches_yml) as f:
        pass   # расскоментировать при работе с yaml
       #templates = yaml.load(f)
        templates ={'sw1': 'London, 21 New Globe Walk'}
    #pprint.pprint(templates)

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

def add_data(db_filename, dhcp_snoop_files):
    if dhcp_snoop_files:
            for dhcp_file in dhcp_snoop_files:
                ins_dhcp(db_filename, dhcp_file)
    else:
        print ('file is not exist')
    return 

def ins_dhcp(db_filename, dhcp_file):
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

def get_all_data(db_filename):
    conn = sqlite3.connect(db_filename)       
    query = 'SELECT * from dhcp'
    result = conn.execute(query)
    print('-' * 80)
    for row in result:
        print ('%-20s'%row[0],'%-15s'%row[1],'%-5s'%row[2],'%-25s'%row[3],'%-5s'%row[4])
        
    
    return

def Control_argument (key, value):
    
    #print (Control_Value (value))
    """ Проверка аргументов и вывод информации по значению"""
    if not key  in keys:
        print('ERROR --  Enter key from {}'.format(', '.join(keys)))
    #elif not Control_Value(value):
    #    print('ERROR --  Value is not correct')
    else:
        get_data (db_filename, key, value)
    
    return
def get_data (db_filename, key, value):
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
    

if __name__ == '__main__':
    db_filename = 'dhcp_snooping.db'
    schema_filename = 'dhcp_snooping_schema.sql'
    create_db(db_filename, schema_filename)