import re
import ipaddress


# 00:A9:BB:3D:D6:58   10.1.10.20   10    FastEthernet0/7      sw2

# исходные данные
#value    = '00:A9:B5B:3D:D6:58'      # [0..9, A..F]
value     = '10.1.10.203434'
#value     = '10.1.10.24'
#value   = '1v$$#%#0' 
#value = '409e6'
#value    = 'FastEthernet01/7'
#value = 'sw2'

# щаблоны регулярных выражений 
regex_mac = re.compile('\w\w\:\w\w\:\w\w\:\w\w\:\w\w\:\w\w')
regex_swich = re.compile('\w+')
regex_eth = re.compile('\d+\/\d+')


a=False                                                     # флаг по умолчанию value не корректно
try:
    print ('1 -control ')
    ip = ipaddress.ip_address(value)                        # проверка на корректность ip adress
    a=True
    #print (ip)
except ValueError:
    try:                                                    # проверка на корректность FastEthernet0/5
       print ('2 -control ')
       value.startswith('FastEthernet')                     # начало строки равно FastEthernet
       match_eth = regex_eth.search(value).group()          
       value.endswith(match_eth)                            # конец строки на соответвие шаблону
       if ('FastEthernet'+(regex_eth.search(value).group())) == value:    # проверка на соответсвие исходной строк, тк шаблон может быть жадным
           a=True
           print ('eth')
    except AttributeError:
        try:                                                # проверка на корректность mac
            print ('3 -control ')
            match_mac = regex_mac.fullmatch(value)          
            if match_mac:
                a=True
                print('mac')
            else:
                try:                                        # проверка на корректность vlan
                    print ('4 -control ')
                    value = int(value)                      # преобразуем занчение к числу и если нет исключения то сравниваем значение
                    if value>=1 and value<=4096:
                        a=True
                    else:
                        print('vlan')
                except ValueError:  
                    pass
                
            if a == False:
                try:                                        # проверка на корректность vlan
                    print ('5 -control ')
                    match_sw = regex_swich.fullmatch(value)
                    if match_sw:
                        a=True
                        print('name')
                except ValueError:
                    pass
        except AttributeError:
            pass


print (a)
