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
            ПРИМЕР Запуска
            $ python3 /home/ubuntu/workspace/python/tasks/6_files/6_2.py config_sw1.txt
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


"""
    ввод информации (имя файла передается как аргумент скрипту)
    обработка файла 
         - исключить строки которые начинаются	с '!'
         - исключить дополнитеьлный символ перевода строки
    вывод обработанной информаци
"""
"""    ввод информации (имя файла передается как аргумент скрипту)
"""
#      ПЕРЕДАЧА АРГУМЕНТОВ СКРИПТУ (argv)
#     обработка файла при этом имя файла передается в качестве параметра

from sys import argv                        # использование argv для работы с аргументами из модуля sys
file_name = argv[1]                         # argv[1] - Это срез списка. (cм ниже )  
                                            # $ python config_sw1.txt   
                                            # argv - это список все аргументы находятся в списке в виде строк
                                            # argv содержит не только аргументы, которые передали скрипту, но и название самого скрипта
                                            # Сначала идет имя самого скрипта, затем аргументы, в том же порядке.
     
file_name="/home/ubuntu/workspace/python/tasks/6_files/"+file_name   # задание пути файла

temp_list_one=[]                                # инициализация вспомогательного списка  
                                            # открытие файла
try:                                        # обработка исключения на наличие файла
    with open(file_name, 'r') as f:
        for line in f:
           #print(line)
           temp_list_one.append(line.rstrip())            # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
except IOError:
    print('No such file')



#print('\n'.join(temp_list_one))                  
"""обработка файла 
      - исключить строки которые начинаются	с '!'
"""
temp_list_two=[]
for x in temp_list_one[1::]:
    if x[0] == '!':
        continue
    else:
        temp_list_two.append(x)





"""    вывод обработанной информаци
"""
print('\n'.join(temp_list_two))
