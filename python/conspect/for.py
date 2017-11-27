# for
"""
строка
функция range()
список
словарь
любой итерируемый объект
вложенные циклы
Совмещение for и if
"""
"""строка
"""
for letter in 'Test string': # letter переменная ипользуемая в цикле
    print(letter)

# for с функцией range(): Range генерирует числа в диапазоне от нуля до
# указанного числа (в данном примере - до 10), не включая его.

"""функция range()
"""
for i in range(10):
    print('interface FastEthernet0/{}'.format(i))

# interface FastEthernet0/0
# interface FastEthernet0/1
# ~~~~~~~~~~~~~~~~~
# interface FastEthernet0/9

"""список
"""

# цикл проходит по списку VLANов, поэтому переменную можно назвать vlan:
vlans = [10, 20, 30, 40, 100]
for vlan in vlans:
    print('vlan {}'.format(vlan))
    print(' name VLAN_{}'.format(vlan))

# vlan 10
# name VLAN_10
# ~~~~~~~~~
# vlan 100
# name VLAN_100
"""словарь
"""
# цикл идет по словарю, то фактически он проходится по ключам
r1 = {
     'IOS': '15.4',
     'IP': '10.255.0.1',
     'hostname': 'london_r1',
     'location': '21 New Globe Walk',
     'model': '4451',
     'vendor': 'Cisco'}
for k in r1:
    print(k)

# vendor
# IP
# hostname
# IOS
# location
# model

#Если необходимо выводить пары ключ-значение в цикле:

for key in r1:
    print(key + ' => ' + r1[key])

# vendor => Cisco
# IP => 10.255.0.1
# hostname => london_r1
# IOS => 15.4
# location => 21 New Globe Walk
# model => 4451  

# В словаре есть специальный метод items, который позволяет проходится в цикле сразу
# по паре ключ:значение:

for key, value in r1.items():
    print(key + ' => ' + value)

# vendor => Cisco
# IP => 10.255.0.1
# hostname => london_r1
# IOS => 15.4
# location => 21 New Globe Walk
# model => 4451

# Метод items возвращает специальный объект view, который отображает пары ключ-значение:

r1.items()
# dict_items

"""вложенные циклы
"""
# в списке commands хранятся команды, которые надо выполнить для
# каждого из интерфейсов в списке fast_int:
commands = ['switchport mode access', 'spanning-tree portfast', 'spanning-tree bpduguard enable']
fast_int = ['0/1','0/3','0/4','0/7','0/9','0/10','0/11']

# Первый цикл for проходится по интерфейсам в списке fast_int, а второй по командам в списке commands
for intf in fast_int:
    print('interface FastEthernet {}'.format(intf))
    for command in commands:
        print(' {}'.format(command))

# interface FastEthernet 0/1
# switchport mode access
# spanning-tree portfast
# spanning-tree bpduguard enable
# ~~~~~~~
"""Совмещение for и if
"""
access_template = ['switchport mode access',
                   'switchport access vlan',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']
fast_int = {'access': { '0/12':10,                 # '0/12':10,  - ключ значение 
                        '0/14':11,
                        '0/16':17,
                        '0/17':150}}
for intf, vlan in fast_int['access'].items():      # перебираются ключи и значения во вложенном словаре fast_int['access']
    print('interface FastEthernet' + intf)         # выводится сторочка interface FastEthernet0/12
    for command in access_template:                # Во втором цикле for перебираются команды из списка access_template  команде switchport access vlan надо добавить номер VLAN
        if command.endswith('access vlan'):        # если команда заканчивается на access vlan
            print(' {} {}'.format(command, vlan))  # выводится команда, и к ней добавляется номер VLAN 
        else:
            print(' {}'.format(command))           # во всех остальных случаях просто выводится команда
# Текущий ключ словаря fast_int, на данный момент цикла, хранится в переменной intf
# Текущее значение словаря fast_int, на данный момент цикла, хранится в переменной vlan           
"""
interface FastEthernet0/12
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/14
 switchport mode access
 switchport access vlan 11
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/16
 switchport mode access
 switchport access vlan 17
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/17
 switchport mode access
 switchport access vlan 150
 spanning-tree portfast
spanning-tree bpduguard enable
"""


#   for/else
# В цикле for: блок else выполняется в том случае, если цикл завершил итерацию списка
# но else не выполняется, если в цикле был выполнен break
# Пример цикла for с else (блок else выполняется после завершения цикла for):
for num in range(5):
    print(num)
else:
    print("Числа закончились")


# Пример цикла for с else и break в цикле (из-за break блок else не выполняется):
for num in range(5):
    if num == 3:
        break
else:
    print(num)
else:
    print("Числа закончились")
    
# Пример цикла for с else и break в цикле (из-за break блок else не выполняется):
for num in range(5):
    if num == 3:
        break
    else:
        print(num)
else:
    print("Числа закончились")
    
# Пример цикла for с else и continue в цикле (continue не влияет на блок else):

for num in range(5):
    if num == 3:
        continue
    else:
        print(num)
else:
    print("Числа закончились")
