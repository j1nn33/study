# Изменить скрипт 7_2.py таким образом, чтобы функция возвращала не список команд, а словарь:
# ключи: имена интерфейсов, вида 'FastEthernet0/1'
# значения: список команд, который надо выполнить на этом интерфейсе

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
    dict_trunc_conf = dict()
    list_trunk_conf = []
    i=0                                                   # переменная для счетчика среза
    for intf in trunk:                                    # пробегаемся по ключам словаря trunk intf пробегается по значениям 0/12
        for command in trunk_template:                    # выбираем команды из trunk_template 
            if command.endswith('allowed vlan'):          # если команда оканчивается на 'access vlan'  добавить vlan
                list_trunk_conf.append('{} {}'.format(command, trunk_dict[intf]))
            else:
                list_trunk_conf.append('{}'.format(command))
        dict_trunc_conf ["interface" + intf] = list_trunk_conf[i:i+4:] 
        i=i+len(trunk_template)                                              
    print (dict_trunc_conf)
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