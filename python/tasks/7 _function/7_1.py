#       Создать функцию, которая генерирует конфигурацию для access-портов.
#            - Параметр access ожидает, как аргумент, словарь access-портов
#            - Функция должна возвращать список всех портов в режиме access с конфигурацией на основе шаблона access_template.
#            - В конце строк в списке не должно быть символа перевода строки.
#           Пример итогового списка см ниже 
      
def generate_access_config(access):
    list_access_conf = []
    for intf in access:                                  # пробегаемся по ключам словаря access intf пробегается по значениям 0/12
        #print('interface FastEthernet' + intf)           # выводм значение ключа intf с пояснениями    
        list_access_conf.append('\'interface FastEthernet' + intf+'\'')
        for command in access_template:                  # выбираем команды из access_template 
            if command.endswith('access vlan'):          # если команда оканчивается на 'access vlan'  добавить vlan
                list_access_conf.append('\' {} {}'.format(command, access[intf])+'\'')
                #print(' {} {}'.format(command, access[intf]))
            else:
                list_access_conf.append('\' {}'.format(command)+'\'')
                #print(' {}'.format(command))
    print ('\n'.join(list_access_conf))
     
   
 
                                            # шаблон access_template
access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']
                                            # словарь access-портов
access_dict = { 'FastEthernet0/12':10,
                'FastEthernet0/14':11,
                'FastEthernet0/16':17,
                'FastEthernet0/17':150 }
                
generate_access_config(access_dict)
"""

[
# 'interface FastEthernet0/12',
# 'switchport mode access',
# 'switchport access vlan 10',
# 'switchport nonegotiate',
# 'spanning-tree portfast',
# 'spanning-tree bpduguard enable',
# 'interface FastEthernet0/17',
# 'switchport mode access',
# 'switchport access vlan 150',
# 'switchport nonegotiate',
# 'spanning-tree portfast',
# 'spanning-tree bpduguard enable',
#     ]
"""