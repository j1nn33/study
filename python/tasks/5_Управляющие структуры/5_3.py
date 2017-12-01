# В скрипте сделан генератор конфигурации для access-портов.
# Сделать аналогичный генератор конфигурации для портов trunk.
# В транках ситуация усложняется тем, что VLANов может быть много, и надо понимать,
# что с ними делать.
# Поэтому в соответствии каждому порту стоит список и первый (нулевой) элемент
# списка указывает как воспринимать номера VLANов, которые идут дальше:
#   add  - значит VLANы надо будет добавить (команда switchport trunk allowed vlan add 10,20)
#   del  - значит VLANы надо удалить из списка разрешенных (команда switchport trunk allowed vlan remove 17)
#   only - значит, что на интерфейсе должны остаться разрешенными только
#          указанные VLANы (команда switchport trunk allowed vlan 11,30)
#   Задача для портов 0/1, 0/2, 0/4:
#   сгенерировать конфигурацию на основе шаблона trunk_template
#   с учетом ключевых слов add, del, only

access_template = ['switchport mode access',
                   'switchport access vlan',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']
trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk allowed vlan']
fast_int = {'access':{'0/12':'10','0/14':'11','0/16':'17','0/17':'150'},
            'trunk':{'0/1':['add','10','20'],
                     '0/2':['only','11','30'],
                     '0/4':['del','17']} }
                     
for intf, vlan in fast_int['access'].items():        # intf, vlan робегается значениям 'access'
    print('interface FastEthernet' + intf)           # intf пробегается по значениям 0/12, 0/14, 0/16, 0/17 
    for command in access_template:                  # выбираем команды из access_template 
        if command.endswith('access vlan'):          # если команда оканчивается на 'access vlan'  добавить vlan
            print(' {} {}'.format(command, vlan))
        else:
            print(' {}'.format(command))             # выводиться команда из списка access_template
        
            
#################################################

"""
 add  - switchport trunk allowed vlan add 10,20
 del  - switchport trunk allowed vlan remove 17
 only - switchport trunk allowed vlan 11,30
"""
vlan_list = ['only','11','30']
#################################################

for intf, vlan_list in fast_int['trunk'].items():      # intf, vlan робегается значениям 'trunk'
    print('interface GigabitEthernet' + intf)          # intf пробегается по значениям 0/1, 0/2, 0/4 
    for command in trunk_template:                     # выбираем команды из trunk_template
        if command.endswith('allowed vlan'):           # если команда оканчивается на 'access vlan'  добавить vlan
            # обработка списка порта в строку в зависмости от параметорв
            # проверить на команду del only
            if vlan_list[0] == 'del':
                result_vlan ='remove '+' '.join(vlan_list[1:])
            elif vlan_list[0] == 'only':
                result_vlan=' '.join(vlan_list[1:])
            else:
                result_vlan=' '.join(vlan_list)
            
            print(' {} {}'.format(command, result_vlan))
        else:
            print(' {}'.format(command))          # выводиться команда из списка access_template





"""           
interface FastEthernet0/17
 switchport mode access
 switchport access vlan 150
 spanning-tree portfast
 spanning-tree bpduguard enable
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


interface GigabitEthernet0/4
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan remove 17
interface GigabitEthernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan add 10 20
interface GigabitEthernet0/2
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan 11 30

 """
 
 
