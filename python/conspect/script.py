#!/usr/bin/env python3
access_template = ['switchport mode access',
'switchport access vlan {}',
'switchport nonegotiate',
'spanning-tree portfast',
'spanning-tree bpduguard enable']
print('\n'.join(access_template).format(5))


"""
    1 name.py - имя файла
    2 LINUX  
            в первой строке файла должна находиться строка 
            #!/usr/bin/env python или
            #!/usr/bin/env python3 , в зависимости от того, какая версия Python используется по умолчанию
            
    3 сделать файл исполняемым (для linux)
            chmod +x name.py
    4 исполнить файл 
            $ ./name.py
            
"""
####################################################################
#      ПЕРЕДАЧА АРГУМЕНТОВ СКРИПТУ (argv)

#    обработка файла при этом имя файла передается в качестве параметра

from sys import argv                        # использование argv для работы с аргументами из модуля sys
interface, vlan = argv[1:]                  # argv[1:] - Это срез списка. (cм ниже )  То есть, в правой
                                            # стороне остается список с двумя элементами: ['Gi0/7', '4'] .

access_template = ['switchport mode access',
'switchport access vlan {}',
'switchport nonegotiate',
'spanning-tree portfast',
'spanning-tree bpduguard enable']
print('interface {}'.format(interface))
print('\n'.join(access_template).format(vlan))


"""
$ python access_template_argv.py Gi0/7 4    
    interface Gi0/7
    switchport mode access
    switchport access vlan 4
    switchport nonegotiate
    spanning-tree portfast
    spanning-tree bpduguard enable
"""

# argv - это список все аргументы находятся в списке в виде строк
# argv содержит не только аргументы, которые передали скрипту, но и название самого скрипта
# Сначала идет имя самого скрипта, затем аргументы, в том же порядке.

#  ['access_template_argv.py', 'Gi0/7', '4']


# Как работает присваивание 

a = 5
b = 6
# оддно и то же 
c, d = 5, 6

# Если вместо чисел список, как в случае с argv:
arg = ['Gi0/7', '4']
interface, vlan = arg

interface
# 'Gi0/7'
vlan
#'4'

###################################
#   Ввод информации пользователем

#     используется функция input() :
print(input('Твой любимый протокол маршрутизации? '))
# Твой любимый протокол маршрутизации? OSPF
# OSPF

#  Сохранить ввод в какой либо переменной 
protocol = input('Твой любимый протокол маршрутизации? ')
# Твой любимый протокол маршрутизации? OSPF
print(protocol)
# OSPF

# Запрос информации из скрипта (файл access_template_input.py):
interface = input('Enter interface type and number: ')
vlan = input('Enter VLAN number: ')
access_template = ['switchport mode access',
                   'switchport access vlan {}',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']
print('\n' + '-' * 30)        #  отделить запрос информации от вывода 
print('interface {}'.format(interface))
print('\n'.join(access_template).format(vlan))

"""
$ python access_template_input.py
Enter interface type and number: Gi0/3
Enter VLAN number: 55
------------------------------
interface Gi0/3
switchport mode access
switchport access vlan 55
switchport nonegotiate
spanning-tree portfast
spanning-tree bpduguard enable
"""

