"""
Теперь создается не только парсер, как в  примере ping_function_ver2 , но и вложенные парсеры.
Вложенные парсеры будут отображаться как команды.
Но, фактически, они будут использоваться как обязательные аргументы.
С помощью вложенных парсеров создается иерархия аргументов и опций.
Аргументы, которые добавлены во вложенный парсер, будут доступны как аргументы этого парсера.
"""
# -*- coding: utf-8 -*-
import argparse

# Default values:
DFLT_DB_NAME = 'dhcp_snooping.db'
DFLT_DB_SCHEMA = 'dhcp_snooping_schema.sql'

# Функция create получает как аргумент все аргументы, которые были переданы. create_parser
# И внутри функции можно обращаться к нужным:
def create(args):
    print('Creating DB {} with DB schema {}'.format((args.name, args.schema)))


def add(args):
    if args.sw_true:
        print('Adding switch data to database')
    else:
        print('Reading info from file(s) \n{}'.format(', '.join(args.filename)))
        print('\nAdding data to db {}'.format(args.db_file))


def get(args):
    if args.key and args.value:
        print('Geting data from DB: {}'.format(args.db_file))
        print('Request data for host(s) with {} {}'.format((args.key, args.value)))
    elif args.key or args.value:
        print('Please give two or zero args\n')
        print(show_subparser_help('get'))
    else:
        print('Showing {} content...'.format(args.db_file))


parser = argparse.ArgumentParser()                                  # создание парсера
                                                                    # создание структуры вложенности
subparsers = parser.add_subparsers(title='subcommands',              
                                   description='valid subcommands',
                                   help='description')

# задание аргумекнтов
create_parser = subparsers.add_parser('create_db', help='create new db')
# metavar позволяет указывать имя аргумента для вывода в сообщении usage и help
create_parser.add_argument('-n', metavar='db-filename', dest='name',
                           default=DFLT_DB_NAME, help='db filename')
create_parser.add_argument('-s', dest='schema', default=DFLT_DB_SCHEMA,
                           help='db schema filename')
# создание базы и вывод значений через функцию или при вызове парсера create_parser будет вызвана функция create
create_parser.set_defaults( func=create )


add_parser = subparsers.add_parser('add', help='add data to db')
# Метод add_argument добавляет аргумент

# nargs позволяет указать, что в этот аргумент должно попасть определенное количество элементов
# В этом случае все аргументы, которые были переданы скрипту после имени аргумента
# filename, попадут в список nargs
# nargs поддерживает такие значения:
# N - должно быть указанное количество аргументов. Аргументы будут в списке
# (даже если указан 1)
# ? - 0 или 1 аргумент
# * - все аргументы попадут в список
# + - все аргументы попадут в список, но должен быть передан хотя бы один аргумент

add_parser.add_argument('filename', nargs='+', help='file(s) to add to db')
add_parser.add_argument('--db', dest='db_file', default=DFLT_DB_NAME, help='db name')
add_parser.add_argument('-s', dest='sw_true', action='store_true',
                        help='add switch data if set, else add normal data')
add_parser.set_defaults( func=add )


get_parser = subparsers.add_parser('get', help='get data from db')
get_parser.add_argument('--db', dest='db_file', default=DFLT_DB_NAME, help='db name')
# choices Для некоторых аргументов важно, чтобы значение было выбрано только из определенных вариантов
get_parser.add_argument('-k', dest='key',
                        choices=['mac', 'ip', 'vlan', 'interface', 'switch'],
                        help='host key (parameter) to search')
get_parser.add_argument('-v', dest='value', help='value of key')
get_parser.add_argument('-a', action='store_true', help='show db content')
get_parser.set_defaults( func=get )



if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)

"""

$ python parse_dhcp_snooping.py -h
usage: parse_dhcp_snooping.py [-h] {create_db,add,get} 

optional arguments:
 -h, --help show this help message and exit
subcommands:
  valid subcommands
  
  {create_db,add,get}   description
   create_db            create new db
   add                  add data to db
   get                  get data from db


У каждого вложенного парсера теперь есть свой help:

$ python parse_dhcp_snooping.py create_db -h
usage: parse_dhcp_snooping.py create_db [-h] [-n db-filename] [-s SCHEMA]

optional arguments:
 -h,    --help          show this help message and exit
 -n     db-filename     db filename
 -s     SCHEMA          db schema filename

"""