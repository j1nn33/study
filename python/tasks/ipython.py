#################################7.3_a


"""Логика работы скрипта
1. открытие файла (с проверками на существование и преобразование его в список)
2. алгоритм парсера
  - если interface FastEthernet
        если начало сторки switchport access vlan то 
        если начало строки switchport trunk allowed vlan то 
        иначе ничего 
  - вывод в функции
"""


from sys import argv 
def get_int_vlan_map(in_cfg):

    temp_list=[]                                  # открытие файла
    try:                                          # обработка исключения на наличие файла
        with open(in_cfg, 'r') as f:
            for line in f:
               temp_list.append(line.rstrip())  # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('---FUNCTION---No such file')

# инициаализация словарей и списков
    d_access = dict()
    d_trunk = dict()
    l_vlan = []
# алгритм парсера
    
    for elelst in temp_list:
        if elelst.startswith('interface FastEthernet'):
            a = elelst[10:26]                               # получение  FastEthernet0/Х
            #print('a равно ', a)
        elif elelst.startswith(' switchport mode access'): 
            b = 1
            d_access[a] = b 
        elif elelst.startswith(' switchport trunk allowed vlan'):
            c=len(' switchport trunk allowed vlan ')
            b = elelst[c::1]                                # получение из строчки switchport trunk allowed vlan значений VLAN
            l_vlan = sorted(b.split(' '))                   # преобразование строки со списком vlan в список 
            #print (l_vlan)
            d_trunk[a] = l_vlan                             # заполнение списка d_access (а ключи  -  будут разными тк FastEthernet0/Х)
            #print ('d_access')
            
        elif elelst.startswith(' switchport access vlan'):  # перезаписываем значение vlan1 в словаре по ключу FastEthernet0/Х  
            c=len(' switchport access vlan ')
            b = elelst[c::1]                                # получение из строчки switchport access vlan Х значения  Х
            #print ('b = ',b)
            d_access[a] = b                                 # заполнение списка d_access (а ключи  -  будут разными тк FastEthernet0/Х)
        else:
            pass
                                                            # ВЫВОД
    print('  PART 2  - COMPLETE ')
    print ('cловарь портов в режиме access')
    print (d_access)                                        
    print ('словарь портов в режиме trunk')
    print (d_trunk)                                         
    return

""" ВЫВОД
cловарь портов в режиме access
{'FastEthernet1/0': '20', 'FastEthernet0/0': '10', 'FastEthernet1/3': 1, 'FastEthernet1/1': '30', 'FastEthernet2/1': 1, 'FastEthernet2/0': 1, 'FastEthernet0/2': '20'}
словарь портов в режиме trunk
{'FastEthernet0/1': ['100,200'], 'FastEthernet0/3': ['100,300'], 'FastEthernet1/2': ['400,500']}
"""
###############################

#################################7.2


# Создать функцию, которая генерирует конфигурацию для trunk-портов.
#            Параметр trunk - это словарь trunk-портов.
#            Словарь trunk имеет такой формат (тестовый словарь trunk_dict уже создан):
# Функция должна возвращать список команд с конфигурацией на основе указанных
# портов и шаблона trunk_template.
# В конце строк в списке не должно быть символа перевода строки.
"""
def generate_trunk_config(trunk_command, *trunk):
    print ('####### in the function ########')
"""   
"""
    for intf in trunk:
        print ('interface ' + intf)                         # вывод ключа          
        #print ('vlan_list' + str(trunk_dict.values()))
        print ('vlan_list_eth'+ str(trunk_dict[intf]))      # вывод значения по ключю 
    for intf in trunk_command: 
        print ('command ' + intf)
"""
"""
    print ('####### RESULT ########')
    list_trunk_conf = []
    for intf in trunk:                                  # пробегаемся по ключам словаря trunk intf пробегается по значениям 0/12
        print('interface ' + intf)                      # выводм значение ключа intf с пояснениями    
        list_trunk_conf.append('\'interface FastEthernet' + intf+'\'')
        #key = intf
        #list_trunk_conf = []
        for command in trunk_template:                   # выбираем команды из trunk_template 
            if command.endswith('allowed vlan'):          # если команда оканчивается на 'access vlan'  добавить vlan
                list_trunk_conf.append('\' {} {}'.format(command, trunk_dict[intf])+'\'')
                print(' {} {}'.format(command, trunk_dict[intf]))
            else:
                list_trunk_conf.append('\' {}'.format(command)+'\'')
                print(' {}'.format(command))
    print ('\n'.join(list_trunk_conf))
    return
################----MAIN PROGRAMM----##############################


trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']
trunk_dict = { 'FastEthernet0/1':[10,20,30],
               'FastEthernet0/2':[11,30],
               'FastEthernet0/4':[17] }

generate_trunk_config(trunk_template, *trunk_dict)      # вызов функции

"""


"""
print ('*********КОНТРОЛЬ параметров при вызове функции ******************************')
for intf in trunk_dict:
    print ('interface ' + intf)                         # вывод ключа          
    print ('vlan_list_eth'+ str(trunk_dict[intf]))      # вывод значения по ключю 
for intf in trunk_template: 
    print ('command ' + intf)
"""
"""
####### in the function ########
####### RESULT ########
interface FastEthernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan [10, 20, 30]
interface FastEthernet0/4
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan [17]
interface FastEthernet0/2
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan [11, 30]
'interface FastEthernetFastEthernet0/1'
' switchport trunk encapsulation dot1q'
' switchport mode trunk'
' switchport trunk native vlan 999'
' switchport trunk allowed vlan [10, 20, 30]'
'interface FastEthernetFastEthernet0/4'
' switchport trunk encapsulation dot1q'
' switchport mode trunk'
' switchport trunk native vlan 999'
' switchport trunk allowed vlan [17]'
'interface FastEthernetFastEthernet0/2'
' switchport trunk encapsulation dot1q'
' switchport mode trunk'
' switchport trunk native vlan 999'
' switchport trunk allowed vlan [11, 30]'
"""
