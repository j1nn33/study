"""print
range
sorted
enumerate
zip
all, any
"""

"""print
"""
print(*items, sep=' ', end='\n', file=sys.stdout, flush=False)
# выводит все элементы, разделяя их значением sep, и завершает вывод значением end
# Все элементы, которые передаются как аргументы, конвертируются в строки

# sep параметр
print(1 sep='\n'+'-'*10+'\n')
# 1
# ----------

# end контролирует то, какое значение выведется после вывода всех элементов.

# file контролирует то, куда выводятся значения функции print. По умолчанию поток вывода - sys.stdout.
f = open('result.txt', 'w')
for num in range(10):
    print('Item {}'.format(num), file=f)

f.close()

"""range
"""
# range возвращает неизменяемую последовательность чисел в виде объекта range.
range(stop)
range(start, stop[, step])  # 0 1 2 3 4 

nums = range(5)
3 in nums                   # проверка, входит ли число в диапазон, который описывает range
# True

nums[-1]                    # получить конкретный элемент диапазона
# 4 

nums[:3]                    # поддержка срезов
# range(0, 3)

len(nums)                   # длина диапазона
# 5

min(nums)                   #минимальный элемент
# 0

nums.index(3)
# 2

"""sorted
"""
# возвращает новый отсортированный список, который получен из итерируемого объекта, который был передан как аргумент
 sorted  -  возвращает список.
# При сортировке кортежа, строки или множества также возвращается список:
#Если сортировать список элементов, то возвращается новый список:
list_of_words = ['one', 'two', 'list', '', 'dict']
sorted(list_of_words)
['', 'dict', 'list', 'one', 'two']

# Если передать sorted словарь, функция вернет отсортированный список ключей
reverse
# Флаг reverse позволяет управлять порядком сортировки.

sorted(list_of_words, reverse=True)
# ['two', 'one', 'list', 'dict', '']

key # можно указывать, как именно выполнять сортировку.
# Параметр key ожидает функцию, с помощью которой должно быть выполнено сравнение.
# образом можно отсортировать список строк по длине строки
sorted(list_of_words, key=len)
# ['', 'one', 'two', 'list', 'dict']

# Параметру key можно передавать любые функции, не только встроенные.  lambda.
# С помощью параметра key можно сортировать объекты не по первому элементу, а по
# любому другому. Но для этого надо использовать или функцию lambda, или
# специальные функции из модуля operator.

# Например, чтобы отсортировать список кортежей из двух элементов по второму
# элементу, надо использовать такой прием:
from operator import itemgetter
list_of_tuples = [('IT_VLAN', 320),
                  ('Mngmt_VLAN', 99),
                  ('User_VLAN', 1010),
                  ('DB_VLAN', 11)]
sorted(list_of_tuples, key=itemgetter(1))
# [('DB_VLAN', 11), ('Mngmt_VLAN', 99), ('IT_VLAN', 320), ('User_VLAN', 1010)]

"""enumerate
"""
# итератор enumerate() аналог дополнительной переменной, которая будет расти на единицу с каждым прохождением цикла
# Сравните:
idx = 0
for item in sequence:
    print(idx)
    idx += 1

# и
for idx, item in enumerate(sequence):
    print(idx)




list1 = ['str1', 'str2', 'str3']
for position, string in enumerate(list1):
    print(position, string)
# 0 str1

#enumerate() умеет считать не только с нуля, но и с любого значение, которое ему указали после объекта

for position, string in enumerate(list1, 100):
    print(position, string)

# 100 str1

# проверить, что сгенерировал итератор. 
list(enumerate(list1, 100))
# [(100, 'str1'), (101, 'str2'), (102, 'str3')]

#Выглядит applet EEM так:
event manager applet Fa0/1_no_shut
event syslog pattern "Line protocol on Interface FastEthernet0/0, changed state to down"
action 1 cli command "enable"
action 2 cli command "conf t"
action 3 cli command "interface fa0/1"
action 4 cli command "no sh"


# генерировать команды EEM на основании существующего списка команд (файл enumerate_eem.py)
# команды считываются из файла, а затем к каждой строке добавляется приставка, которая нужна для EEM.
import sys
config = sys.argv[1]
with open(config, 'r') as f:
    for i, command in enumerate(f, 1):
        print('action {:04} cli command "{}"'.format(i, command.rstrip()))
   
"""r1_config.txt

en
conf t
no int Gi0/0/0.300
no int Gi0/0/0.301
no int Gi0/0/0.302
int range gi0/0/0-2
channel-group 1 mode active
interface Port-channel1.300
encapsulation dot1Q 300
vrf forwarding Management
ip address 10.16.19.35 255.255.255.248
"""

$ python enumerate_eem.py r1_config.txt
action 0001 cli command "en"
action 0002 cli command "conf t"
action 0003 cli command "no int Gi0/0/0.300"
action 0004 cli command "no int Gi0/0/0.301"
action 0005 cli command "no int Gi0/0/0.302"
action 0006 cli command "int range gi0/0/0-2"
action 0007 cli command " channel-group 1 mode active"
action 0008 cli command "interface Port-channel1.300"
action 0009 cli command " encapsulation dot1Q 300"
action 0010 cli command " vrf forwarding Management"
action 0011 cli command " ip address 10.16.19.35 255.255.255.248"


"""zip
"""
# на вход функции передаются последовательности
# zip() возвращает итератор с кортежами, в котором n-ый кортеж состоит из n-ых
#  элементов последовательностей, которые были переданы как аргументы
#  например, десятый кортеж будет содержать десятый элемент каждой из переданных последовательностей
# если на вход были переданы последовательности разной длины, то все они будут отрезаны по самой короткой последовательности
# порядок элементов соблюдается

# Так как zip - это итератор, для отображение его содержимого используется list()

a = [1,2,3]
b = [100,200,300]
list(zip(a,b))
# [(1, 100), (2, 200), (3, 300)]

#Использование zip для создания словаря:

d_keys = ['hostname', 'location', 'vendor', 'model', 'IOS', 'IP']
d_values = ['london_r1', '21 New Globe Walk', 'Cisco', '4451', '15.4', '10.255.0.1']
list(zip(d_keys,d_values))
# [('hostname', 'london_r1'),
# ('location', '21 New Globe Walk'),
# ('vendor', 'Cisco'),
# ('model', '4451'),
# ('IOS', '15.4'),
# ('IP', '10.255.0.1')]

r1 = dict(zip(d_keys,d_values))
print(r1)
# {'IOS': '15.4',
# 'IP': '10.255.0.1',
# 'hostname': 'london_r1',
# 'location': '21 New Globe Walk',
# 'model': '4451',
# 'vendor': 'Cisco'}

# В примере ниже есть отдельный список, в котором хранятся ключи, и словарь, в
# котором хранится в виде списка (чтобы сохранить порядок) информация о каждом устройстве.
# Соберем их в словарь с ключами из списка и информацией из словаря data:
d_keys = ['hostname', 'location', 'vendor', 'model', 'IOS', 'IP']
data = {'r1': ['london_r1', '21 New Globe Walk', 'Cisco', '4451', '15.4', '10.255.0.1'],
        'r2': ['london_r2', '21 New Globe Walk', 'Cisco', '4451', '15.4', '10.255.0.2'],
       'sw1': ['london_sw1', '21 New Globe Walk', 'Cisco', '3850', '3.6.XE', '10.255.0.101']
       }
london_co = {}
for k in data.keys():
    london_co[k] = dict(zip(d_keys,data[k]))
print(london_co)
# {'r1': {'IOS': '15.4',
# 'IP': '10.255.0.1',
# 'hostname': 'london_r1',
# 'location': '21 New Globe Walk',
# 'model': '4451',
# 'vendor': 'Cisco'},
# 'r2': {'IOS': '15.4',
# 'IP': '10.255.0.2',
# 'hostname': 'london_r2',
# 'location': '21 New Globe Walk',
# 'model': '4451',
# 'vendor': 'Cisco'},
# 'sw1': {'IOS': '3.6.XE',
# 'IP': '10.255.0.101',
# 'hostname': 'london_sw1',
# 'location': '21 New Globe Walk',
# 'model': '3850',
# 'vendor': 'Cisco'}}
"""all, any
"""
# Функция all() возвращает True, если все элементы истина (или объект пустой).
all([False, True, True])
# False
all([True, True, True])
# True
all([])
# True
# Например, с помощью all можно проверить, все ли октеты в IP-адресе являются числами:
IP = '10.0.1.1'
all( i.isdigit() for i in IP.split('.'))
# True
all( i.isdigit() for i in '10.1.1.a'.split('.'))
# False

# Функция any() возвращает True, если хотя бы один элемент истина.
any([False, True, True])
# True
any([False, False, False])
# False
any([])
# False
any( i.isdigit() for i in '10.1.1.a'.split('.'))
# True

# Например, с помощью any, можно заменить функцию ignore_command:

'''
Функция проверяет содержится ли в команде слово из списка ignore.
command - строка. Команда, которую надо проверить ignore - список. Список слов
Возвращает True, если в команде содержится слово из списка ignore, False - если нет
'''
def ignore_command(command, ignore):
    ignore = ['duplex', 'alias', 'Current configuration']
ignore_command = False
for word in ignore:
    if word in command:
        return True
return ignore_command

# На такой вариант:
'''
Функция проверяет содержится ли в команде слово из списка ignore.
command - строка. Команда, которую надо проверить ignore - список. Список слов
Возвращает True, если в команде содержится слово из списка ignore, False - если нет
'''
def ignore_command(command, ignore):
    ignore = ['duplex', 'alias', 'Current configuration']
return any(word in command for word in ignore)