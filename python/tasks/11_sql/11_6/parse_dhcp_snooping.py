#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import parse_dhcp_snooping_functions as pds

# Default values:
DFLT_DB_NAME = 'dhcp_snooping.db'
DFLT_DB_SCHEMA = 'dhcp_snooping_schema.sql'


def create(args):
    print('Creating DB {} with DB schema {}'.format(args.name, args.schema))
    pds.create_db(args.name, args.schema)


def add(args):
    if args.sw_true:
        print('Adding switch data to database')
        pds.add_data_switches(args.db_file, args.filename)
    else:
        print('Reading info from file(s) \n{}'.format(', '.join(args.filename)))
        print('\nAdding data to db {}'.format(args.db_file))
        pds.add_data(args.db_file, args.filename)


def get(args):
    if args.key and args.value:
        print('Geting data from DB: {}'.format(args.db_file))
        print('Request data for host(s) with {} {}'.format(args.key, args.value))
        pds.get_data(args.db_file, args.key, args.value)
    elif args.key or args.value:
        print('Please give two or zero args\n')
        print(show_subparser_help('get'))
    else:
        print('Showing {} content...'.format(args.db_file))
        pds.get_all_data(args.db_file)


def show_subparser_help(subparser_name):
    '''
    Function returns help message for subparser
    '''
    subparsers_actions = [
        action for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)]
    return subparsers_actions[0].choices[subparser_name].format_help()


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='additional info')


create_parser = subparsers.add_parser('create_db', help='create new db')
create_parser.add_argument('-n', dest='name', default=DFLT_DB_NAME,
                           help='db filename')
create_parser.add_argument('-s', dest='schema', default=DFLT_DB_SCHEMA,
                           help='db schema filename')
create_parser.set_defaults(func=create)


add_parser = subparsers.add_parser('add', help='add data to db')
add_parser.add_argument('filename', nargs='+', help='file(s) to add to db')
add_parser.add_argument('--db', dest='db_file', default=DFLT_DB_NAME, help='db name')
add_parser.add_argument('-s', dest='sw_true', action='store_true',
                        help='add switch data if set, else add normal data')
add_parser.set_defaults(func=add)


get_parser = subparsers.add_parser('get', help='get data from db')
get_parser.add_argument('--db', dest='db_file', default=DFLT_DB_NAME, help='db name')
get_parser.add_argument('-k', dest='key',
                        choices=['mac', 'ip', 'vlan', 'interface', 'switch'],
                        help='host key (parameter) to search')
get_parser.add_argument('-v', dest='value', help='value of key')
get_parser.add_argument('-a', action='store_true', help='show db content')
get_parser.set_defaults(func=get)



if __name__ == '__main__':
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        args.func(args)

#-----------------------------------
"""
--------Проверка скрипта 
cd /home/ubuntu/workspace/python/tasks/11_sql/11_6/
Созданеие базы данных
python3 /home/ubuntu/workspace/python/tasks/11_sql/11_6/parse_dhcp_snooping.py create_db
python3 /home/ubuntu/workspace/python/tasks/11_sql/11_6/parse_dhcp_snooping.py create_db  -n db_namy_my -s myshema
sqlite3 /home/ubuntu/workspace/python/tasks/11_sql/11_6/dhcp_snooping.db "SELECT name FROM sqlite_master WHERE type='table'"                                      
switches
dhcp

добавление данных в базу из таблицы
python3 /home/ubuntu/workspace/python/tasks/11_sql/11_6/parse_dhcp_snooping.py add sw1_dhcp_snooping.txt sw2_dhcp_snooping.txt sw3_dhcp_snooping.txt

получение всех данных из таблицы 
python3 /home/ubuntu/workspace/python/tasks/11_sql/11_6/parse_dhcp_snooping.py get

получение всех выборочных данных из таблицы
$ python3 /home/ubuntu/workspace/python/tasks/11_sql/11_6/parse_dhcp_snooping.py get -k vlan -v 10


--------
скрипт реализует дополнительно вывод функционала  - help 
$ python3 /home/ubuntu/workspace/python/tasks/11_sql/11_6/parse_dhcp_snooping.py -h                                                                                                          
usage: parse_dhcp_snooping.py [-h] {create_db,add,get} ...

optional arguments:
  -h, --help           show this help message and exit

subcommands:
  valid subcommands

  {create_db,add,get}  additional info
    create_db          create new db
    add                add data to db
    get                get data from db
    
$ python3 /home/ubuntu/workspace/python/tasks/11_sql/11_6/parse_dhcp_snooping.py get -h
usage: parse_dhcp_snooping.py get [-h] [--db DB_FILE]
                                  [-k {mac,ip,vlan,interface,switch}]
                                  [-v VALUE] [-a]

optional arguments:
  -h, --help            show this help message and exit
  --db DB_FILE          db name
  -k {mac,ip,vlan,interface,switch}
                        host key (parameter) to search
  -v VALUE              value of key
  -a                    show db content


"""