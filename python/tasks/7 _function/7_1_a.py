# Сделать копию скрипта задания 7_1
# Дополнить скрипт:
# ввести дополнительный параметр, который контролирует будет ли настроен port-security
# имя параметра 'psecurity' по умолчанию значение False
# Проверить работу функции на примере словаря access_dict, с генерацией конфигурации port-security и без.
def generate_access_config(access, psecurity=False):
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
        for command_psecurity in port_security:
            # print (psecurity)
            if psecurity==True:
                list_access_conf.append('\' {}'.format(command_psecurity)+'\'')
            else:
                pass
    print ('\n'.join(list_access_conf))
    return
    
 

 
                                            # шаблон access_template
access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']
                                            # шаблон port_security
port_security = ['switchport port-security maximum 2',              # 2 - mac address разрешено
                 'switchport port-security violation restrict',     # действие на нарушение <protect | restrict | shutdown> 
                 'switchport port-security']                        # включение на интерфейсе 
                                            # словарь access-портов
access_dict = { 'FastEthernet0/12':10,
                'FastEthernet0/14':11,
                'FastEthernet0/16':17,
                'FastEthernet0/17':150 }

a = input('psecurity = Falese, input psecurity ',)      # запрос на ввод параметра psecurity
if a=='True':                                           # вызов функции в зависимости от параметра
    generate_access_config(access_dict, True)          
else:
    generate_access_config(access_dict)
    print ('psecurity = False')

