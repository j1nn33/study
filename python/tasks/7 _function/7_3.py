# Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора и возвращает два объекта:
# словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
#                    {'FastEthernet0/12':10,
#                    'FastEthernet0/14':11,
#                    'FastEthernet0/16':17}
# словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
#                    {'FastEthernet0/1':[10,20],
#                    'FastEthernet0/2':[11,30],
#                    'FastEthernet0/4':[17]}
# Функция ожидает в качестве аргумента имя конфигурационного файла. config_sw1.txt

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
        with open('/home/ubuntu/workspace'+in_cfg, 'r') as f:
            for line in f:
               temp_list.append(line.rstrip())  # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('No such file')

    #print('\n'.join(temp_list)) 
# инициаализация словарей и списков
    d_access = dict()
    d_trunk = dict()
    l_vlan = []
# алгритм парсера
    for elelst in temp_list:
        if  elelst.startswith('interface FastEthernet'):
            a = elelst[10:26]                               # получение  FastEthernet0/Х
            #print('a равно ', a)
        elif elelst.startswith(' switchport access vlan'):
            c=len(' switchport access vlan ')
            b = elelst[c::1]                                # получение из строчки switchport access vlan Х значения  Х
            #print ('b = ',b)
            d_access[a] = b                                 # заполнение списка d_access (а ключи  -  будут разными тк FastEthernet0/Х)
            #print (d_access)
            #print ('a_access')
        elif elelst.startswith(' switchport trunk allowed vlan'):
            c=len(' switchport trunk allowed vlan ')
            b = elelst[c::1]                                # получение из строчки switchport trunk allowed vlan значений VLAN
            l_vlan = sorted(b.split(' '))                   # преобразование строки со списком vlan в список 
            #print (l_vlan)
            d_trunk[a] = l_vlan                                 # заполнение списка d_access (а ключи  -  будут разными тк FastEthernet0/Х)
            #print ('d_access')
        else:
            pass
                                                            # ВЫВОД
    print ('cловарь портов в режиме access')
    print (d_access)                                        
    print ('словарь портов в режиме trunk')
    print (d_trunk)                                         
    return
 
get_int_vlan_map('/python/tasks/7 _function/config_sw1.txt')