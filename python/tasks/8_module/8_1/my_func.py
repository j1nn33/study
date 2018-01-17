# функции из заданий:
# - 7.1a
# - 7.2
# - 7.3a    
################################# tesing func
def testing():
    print ('test sucsessfull')
    return
#testing()

#################################7.1_a
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
    return list_access_conf

#################################7.2
   
def generate_trunk_config_with_template(trunk_command, trunk):
    list_trunk_conf = []
    for intf in trunk:                                  # пробегаемся по ключам словаря trunk intf пробегается по значениям 0/12
        list_trunk_conf.append('\'interface FastEthernet' + intf+'\'')
        for command in trunk_template:                   # выбираем команды из trunk_template 
            if command.endswith('allowed vlan'):          # если команда оканчивается на 'access vlan'  добавить vlan
                list_trunk_conf.append('\' {} {}'.format(command, trunk[intf])+'\'')
            else:
                list_trunk_conf.append('\' {}'.format(command)+'\'')
    return list_trunk_conf
    
   
################----MAIN PROGRAMM----##############################

trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']

def generate_trunk_config(trunk_dict):
    list_trunk_conf = generate_trunk_config_with_template(trunk_template, trunk_dict)  
    return list_trunk_conf


#################################7.3_a
def get_int_vlan_map(in_cfg):
    temp_list=[]                                            # открытие файла
    try:                                                    # обработка исключения на наличие файла
        with open(in_cfg, 'r') as f:
            for line in f:
               temp_list.append(line.rstrip())              # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
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
        elif elelst.startswith(' switchport mode access'): 
            b = 1
            d_access[a] = b 
        elif elelst.startswith(' switchport trunk allowed vlan'):
            c=len(' switchport trunk allowed vlan ')
            b = elelst[c::1]                                # получение из строчки switchport trunk allowed vlan значений VLAN
            l_vlan = sorted(b.split(' '))                   # преобразование строки со списком vlan в список 
            d_trunk[a] = l_vlan                             # заполнение списка d_access (а ключи  -  будут разными тк FastEthernet0/Х)
        elif elelst.startswith(' switchport access vlan'):  # перезаписываем значение vlan1 в словаре по ключу FastEthernet0/Х  
            c=len(' switchport access vlan ')
            b = elelst[c::1]                                # получение из строчки switchport access vlan Х значения  Х
            d_access[a] = b                                 # заполнение списка d_access (а ключи  -  будут разными тк FastEthernet0/Х)
        else:
            pass
                                                            # ВЫВОД
    print('  PART 2  - COMPLETE  in function ')
    #print ('in funk cловарь портов в режиме access')
    #print (d_access)                                        
    #print ('in funk словарь портов в режиме trunk')
    #print (d_trunk)                                         
    return (d_access, d_trunk)

###############################
if __name__ == '__main__':
    main()