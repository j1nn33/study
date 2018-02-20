"""
subprocess
os
argparse
ipaddress
pprint
tabulate
"""

"""subprocess  см пример 8_3
"""
# Модуль subprocess позволяет создавать новые процессы.

# С помощью subprocess можно, например, выполнять любые команды Linux из скрипта.
# И, в зависимости от ситуации, получать вывод или только проверять, что команда
# выполнилась без ошибок

import subprocess
result = subprocess.call('ls')

# В переменной result теперь содержится специальный объект CompletedProcess. Из
# этого объекта можно получить информацию о выполнении процесса, например, о коде возврата:
result
# CompletedProcess(args='ls', returncode=0)
result.returncode
# 0                   Код 0 означает, что программа выполнилась успешно.

# если необходимо вызвать команду с аргументами, её нужно передавать таким образом (как список):
result = subprocess.call(['ls', '-ls'])

# При попытке выполнить команду с использованием wildcard выражений, например, использовать * , возникнет ошибка:
result = subprocess.call(['ls', '-ls', '*md'])
# ls: cannot access *md: No such file or directory
# Чтобы вызывать команды, в которых используются wildcard выражения, нужно добавлять аргумент shell и вызывать команду таким образом:
result = subprocess.call('ls -ls *md', shell=True)
result = subprocess.call(['ping', '-c', '3', '-n', '8.8.8.8'])

# Получение результата выполнения команды

#По умолчанию функция run возвращает результат выполнения команды на стандартный поток вывода.
#Если нужно получить результат выполнения команды, надо добавить аргумент stdout и указать ему значение subprocess.PIPE:

result = subprocess.call(['ls', '-ls'], stdout=subprocess.PIPE
print(result.stdout)

# b'total 28\n4 -rw-r--r-- 1            b - еред строкой. Она означает, что модуль вернул вывод в виде байтовой строки.
# Для перевода её в unicode есть два варианта: выполнить decode полученной строки; указать аргумент encoding
print(result.stdout.decode('utf-8'))
result = subprocess.call(['ls', '-ls'], stdout=subprocess.PIPE, encoding='utf-8')
print(result.stdout)

result = subprocess.call(['ls', '-ls'], stdout=subprocess.DEVNULL) # отключение вывода, но можно получить код возврата
print(result.stdout)
# None
print(result.returncode)
# 0       Код 0 означает, что программа выполнилась успешно.

# Работа со стандартным потоком ошибок

# Если команда была выполнена с ошибкой или не отработала корректно, вывод команды попадет на стандартный поток ошибок

result = subprocess.call(['ping', '-c', '3', '-n', 'a'], stderr=subprocess.PIPE, encoding='utf-8')

# Теперь в result.stdout пустая строка, а в result.stderr находится стандартный поток вывода:
print(result.stdout)
# None
print(result.stderr)
# ping: unknown host a
print(result.returncode)
# 2

# пример    см пример 8_3
import subprocess


def ping_ip(ip_address):
    '''
    Ping IP address and return tuple:
    On success:
        * True
        * command output (stdout)
    On failure:
        * False
        * error output (stderr)
    '''
    reply = subprocess.call(['ping', '-c', '3', '-n', ip_address],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding='utf-8')
    if reply.returncode == 0:
        return True, reply.stdout
    else:
        return False, reply.stderr

print(ping_ip('8.8.8.8'))
print(ping_ip('a'))

# Пример 2 см пример 8_3

import subprocess

def ping_ip(ip_address):

    if  subprocess.call (['ping','-c','3',ip_address]) ==0:
        print ('yes')
    else:
        print ('no')
    return


ping_ip('192.168.40.254')

"""os Модуль os позволяет работать с файловой системой, с окружением, управлять процессами.
"""
import os
os.mkdir('test')                 # создать каталог

if not os.path.exists('test'):   # проверка на существовавние каталога
    os.mkdir('test')

os.listdir('.')                  # просмотр каталога
print (os.listdir('.') )  
['6_files', '3_Типы данных', '7 _function', 'ipython.py', '4_Базовые скрипты', '5_Управляющие структуры']

# С помощью проверок os.path.isdir и os.path.isfile можно получить отдельно список файлов и список каталогов:
dirs = [ d for d in os.listdir('.') if os.path.isdir(d)]
print (dirs)
# ['dir2', 'dir3', 'test']
files = [ f for f in os.listdir('.') if os.path.isfile(f)]
print (files)
# ['cover3.png', 'README.txt']

# методы для работы с путями:

os.path.basename(file)
# 'README.md'
os.path.dirname(file)
# 'Programming/PyNEng/book/16_additional_info'
os.path.split(file)
# ('Programming/PyNEng/book/16_additional_info', 'README.md')



"""argparse  
     
     это модуль для обработки аргументов командной строки
   - создавать аргументы и опции, с которыми может вызываться скрипт
   - указывать типы аргументов, значения по умолчанию
   - указывать, какие действия соответствуют аргументам
   - выполнять вызов функции при указании аргумента
   - отображать сообщения с подсказками по использованию скрипта
"""
import argparse

                                                # Создание парсера:
parser = argparse.ArgumentParser(description='Ping script')
                                                # Добавление аргументов:
parser.add_argument('-a', action="store", dest="ip")
                    # аргумент, который передается после опции -a , сохранится в переменную ip

args = parser.parse_args()                      # указывается после того, как определены все аргументы.
                                # После её выполнения в переменной args содержатся все аргументы, которые были
                                # переданы скрипту. К ним можно обращаться, используя синтаксис args.ip .

# Остановимся на действиях (actions). Они могут быть следующими:
#                                    store — действие по умолчанию;
#                                    store_const: в основном используется для флагов.
#                                    Либо вернет Вам значение, указанное в const, либо (если ничего не указано), None.

# store_true / store_false: аналог store_const, но для булевых True и False;
# append: возвращает список путем добавления в него значений агрументов.
# append_const: возвращение значения, определенного в спецификации аргумента, в список.
# count: как следует из названия, считает, сколько раз встречается значение данного арг#умента. 

#
#
#

# ПРИМЕР

import subprocess
from tempfile import TemporaryFile   # требуется создать временный файл, который после выполнения некоторых действий больше не нужен

import argparse


def ping_ip(ip_address, count):
    '''
    Ping IP address and return tuple:
    On success: (return code = 0, command output)
    On failure: (return code, error output (stderr))
    '''
    with TemporaryFile() as temp:                 
        try:
            output = subprocess.check_output(['ping', '-c', str(count), '-n', ip_address],
                                             stderr=temp)
            return 0, output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            temp.seek(0)
            return e.returncode, temp.read().decode('utf-8')


parser = argparse.ArgumentParser(description='Ping script')    # Создание парсера:

# Добавление аргументов
# аргумент, который передается после опции -a , сохранится в переменную ip
parser.add_argument('-a', action='store', dest='ip', required=True)    #  required=True - что опция указывается обязательно 
# аргумент, который передается после опции -c , будет сохранен в переменную
# count , но, прежде, будет конвертирован в число. Если аргумент не было
# указан, по умолчанию будет значение 2
parser.add_argument('-c', action='store', dest='count', default=2, type=int)

args = parser.parse_args()
# После выполнения  args = parser.parse_args() в переменной args 
# содержатся все аргументы, которые были переданы скрипту.
# К ним можно обращаться, используя синтаксис args.ip .
print(args)

rc, message = ping_ip( args.ip, args.count )
print(message)


"""
вызовы функции

$ python ping_function.py -a 8.8.8.8 -c 5
# Namespace(count=5, ip='8.8.8.8')

$ python ping_function.py -a 8.8.8.8
# Namespace(count=2, ip='8.8.8.8')


"""

"""ipaddress
"""
ipaddress.ip_address() # позволяет создавать объект IPv4Address или IPv6Address соответственно.
import ipaddress
ipv4 = ipaddress.ip_address('10.0.1.1')
print(ipv4)
# 10.0.1.1

ip1 = ipaddress.ip_address('10.0.1.1')
ip2 = ipaddress.ip_address('10.0.2.1')
ip1 > ip2
# False

str(ip1)
# '10.0.1.1'
int(ip1)
# 167772417
ip1 + 5
# IPv4Address('10.0.1.6')

subnet1 = ipaddress.ip_network('80.0.1.0/28')    # создает объекты описывающие сеть

subnet1.broadcast_address
# IPv4Address('80.0.1.15')
subnet1.with_netmask
# '80.0.1.0/255.255.255.240'
subnet1.with_hostmask
# '80.0.1.0/0.0.0.15'
subnet1.prefixlen
# 28
subnet1.num_addresses
# 16
print(list(subnet1.hosts()))

# [IPv4Address('80.0.1.1'),
#  IPv4Address('80.0.1.2')
#

print(list(subnet1.subnets(prefixlen_diff=2)))   # разделение сети на подсети с префиксом 2

# [IPv4Network('80.0.1.0/30'),
#  IPv4Network('80.0.1.4/30'),
#  IPv4Network('80.0.1.8/30'),
#  IPv4Network('80.0.1.12/30')]

for ip in subnet1:             # проход по адресам в подсети
    print(ip)
    
subnet1[0]                     # обращение к определенному адресу в подсетке
# IPv4Address('80.0.1.0')
subnet1[5]
# IPv4Address('80.0.1.5')

ip1 = ipaddress.ip_address('80.0.1.3')  # Таким образом можно проверять, находится ли IP-адрес в сети:
print (ip1 in subnet1) 
# True

ipaddress.ip_interface()          # Функция ipaddress.ip_interface() позволяет создавать объект IPv4Interface или IPv6Interface соответственно.

int1 = ipaddress.ip_interface('10.0.1.1/24') # создать интерфейс
int1.ip
# IPv4Address('10.0.1.1')
int1.network
# IPv4Network('10.0.1.0/24')
int1.netmask
# IPv4Address('255.255.255.0')

# Пример проверки является ли адрес адресом сети или хоста

IP1 = '10.0.1.1/24'
IP2 = '10.0.1.0/24'
def check_if_ip_is_network(ip_address):
    try:
        ipaddress.ip_network(ip_address)
        return True
    except ValueError:
        return False

check_if_ip_is_network(IP1)
False
check_if_ip_is_network(IP2)
True
"""pprint
позволяет красиво отображать объекты Python. При этом сохраняется
структура объекта и отображение, которое выводит pprint, можно использовать для
создания объекта.
"""

from pprint import pprint

print (tunnel)
# '\ninterface Tunnel0\n ip address 10.10.10.1 255.255.255.0\n ip mtu 1416\n ip
# ospf hello-interval 5\n tunnel source FastEthernet1/0\n tunnel protection ipsec profi
# le DMVPN\n'
pprint(tunnel)
#('\n'
#'interface Tunnel0\n'
#' ip address 10.10.10.1 255.255.255.0\n'
#' ip mtu 1416\n'
#' ip ospf hello-interval 5\n'
#' tunnel source FastEthernet1/0\n'
#' tunnel protection ipsec profile DMVPN\n')


# depth позволяет ограничивать глубину отображения структуры данных.
# Можно отобразить только ключи, указав глубину равной 1

# pformat - это функция, которая отображает результат в виде строки. Ее удобно
# использовать, если необходимо записать структуру данных в какой-то файл,
# например, для логирования.



"""tabulate
"""
pip install tabulate

# список списков (в общем случае iterable of iterables)
# список словарей (или любой другой итерируемый объект со словарями). Ключи используются как имена столбцов
# словарь с итерируемыми объектами. Ключи используются как имена столбцов

from tabulate import tabulate
sh_ip_int_br = [('FastEthernet0/0', '15.0.15.1', 'up', 'up'),
                ('FastEthernet0/1', '10.0.12.1', 'up', 'up'),
                ('FastEthernet0/2', '10.0.13.1', 'up', 'up'),
                ('Loopback0', '10.1.1.1', 'up', 'up'),
                ('Loopback100', '100.0.0.1', 'up', 'up')]

print(tabulate(sh_ip_int_br))
# --------------- --------- -- --
# FastEthernet0/0 15.0.15.1 up up
# FastEthernet0/1 10.0.12.1 up up
# FastEthernet0/2 10.0.13.1 up up
# Loopback0 10.1.1.1 up up
# Loopback100 100.0.0.1 up up
# --------------- --------- -- --

# headers - позволяет передавать дополнительный аргумент, в котором указаны имена столбцов
columns=['Interface', 'IP', 'Status', 'Protocol']
print(tabulate(sh_ip_int_br, headers=columns))

# Interface IP Status Protocol
# --------------- --------- -------- ----------
# FastEthernet0/0 15.0.15.1 up       up
# FastEthernet0/1 10.0.12.1 up       up
# FastEthernet0/2 10.0.13.1 up       up
# Loopback0       10.1.1.1  up       up
# Loopback100     100.0.0.1 up       up

# часто первый набор данных - это заголовки. достаточно указать headers равным "firstrow":
print (data)

# [('Interface', 'IP', 'Status', 'Protocol'),
# ('FastEthernet0/0', '15.0.15.1', 'up', 'up'),
# ('FastEthernet0/1', '10.0.12.1', 'up', 'up'),
# ('FastEthernet0/2', '10.0.13.1', 'up', 'up'),
# ('Loopback0', '10.1.1.1', 'up', 'up'),
# ('Loopback100', '100.0.0.1', 'up', 'up')]
print(tabulate(data, headers='firstrow'))
# Interface IP Status Protocol
# --------------- --------- -------- ----------
# FastEthernet0/0 15.0.15.1 up       up
# FastEthernet0/1 10.0.12.1 up       up
# FastEthernet0/2 10.0.13.1 up       up
# Loopback0       10.1.1.1  up       up
# Loopback100     100.0.0.1 up       up

# Если данные в виде списка словарей, надо указать headers равным "keys":
print(list_of_dict)
# [{'IP': '15.0.15.1',
# 'Interface': 'FastEthernet0/0',
# 'Protocol': 'up',
# 'Status': 'up'},
# {'IP': '10.0.12.1',
# 'Interface': 'FastEthernet0/1',
# 'Protocol': 'up',
# 'Status': 'up'}]
print(tabulate(list_of_dict, headers='keys'))
# Interface IP Status Protocol
# --------------- --------- -------- ----------
# FastEthernet0/0 15.0.15.1 up up
# FastEthernet0/1 10.0.12.1 up up

# СТИЛИ grid

print(tabulate(list_of_dict, headers='keys', tablefmt="grid"))
#+-----------------+-----------+----------+------------+
#| Interface       | IP        | Status   | Protocol   |
#+=================+===========+==========+============+
#| FastEthernet0/0 | 15.0.15.1 | up       | up         |
#+-----------------+-----------+----------+------------+
#| FastEthernet0/1 | 10.0.12.1 | up       | up         |
#+-----------------+-----------+----------+------------+

print(tabulate(list_of_dict, headers='keys', tablefmt='pipe'))
#| Interface       | IP        | Status   | Protocol   |
#|:----------------|:----------|:---------|:-----------|
#| FastEthernet0/0 | 15.0.15.1 | up       | up         |
#| FastEthernet0/1 | 10.0.12.1 | up       | up         |

# Выравнивание столбцов
print(tabulate(list_of_dict, headers='keys', tablefmt='pipe', stralign='center'))


# Таблица в формате HTML:
print(tabulate(list_of_dict, headers='keys', tablefmt='html'))
# <table>
# <thead>
# <tr><th>Interface </th><th>IP </th><th>Status </th><th>Protocol </th></tr
# >
# </thead>
# <tbody>
# <tr><td>FastEthernet0/0</td><td>15.0.15.1</td><td>up </td><td>up </td></tr
# >
# <tr><td>FastEthernet0/1</td><td>10.0.12.1</td><td>up </td><td>up </td></tr
# >
# </tbody>
# </table>


