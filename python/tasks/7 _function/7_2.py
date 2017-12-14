# Создать функцию, которая генерирует конфигурацию для trunk-портов.
#            Параметр trunk - это словарь trunk-портов.
#            Словарь trunk имеет такой формат (тестовый словарь trunk_dict уже создан):
# Функция должна возвращать список команд с конфигурацией на основе указанных
# портов и шаблона trunk_template.
# В конце строк в списке не должно быть символа перевода строки.

def generate_trunk_config(trunk_command, *trunk):
    print ('####### in the function ########')
    """
    for intf in trunk:
        print ('interface ' + intf)                         # вывод ключа          
        #print ('vlan_list' + str(trunk_dict.values()))
        print ('vlan_list_eth'+ str(trunk_dict[intf]))      # вывод значения по ключю 
    for intf in trunk_command: 
        print ('command ' + intf)
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
""""
print ('*********КОНТРОЛЬ параметров при вызове функции ******************************')
for intf in trunk_dict:
    print ('interface ' + intf)                         # вывод ключа          
    print ('vlan_list_eth'+ str(trunk_dict[intf]))      # вывод значения по ключю 
for intf in trunk_template: 
    print ('command ' + intf)
"""