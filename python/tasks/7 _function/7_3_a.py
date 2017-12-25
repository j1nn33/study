# Сделать копию скрипта задания 7.3.
# добавить поддержку конфигурации, когда настройка access-порта выглядит так: 
#           interface FastEthernet0/20
#           switchport mode access
#           duplex auto
# То есть, порт находится в VLAN 1. В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
#          {'FastEthernet0/12':10,
#          'FastEthernet0/14':11,
#          'FastEthernet0/20':1 }

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
            #print (d_access)
            #print ('a_access')
        else:
            pass
                                                            # ВЫВОД
    print ('cловарь портов в режиме access')
    print (d_access)                                        
    print ('словарь портов в режиме trunk')
    print (d_trunk)                                         
    return
 
get_int_vlan_map('/python/tasks/7 _function/config_sw2.txt')

