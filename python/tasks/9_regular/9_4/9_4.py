"""
Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент имя файла, sh_ip_int_br_2.txt
           в котором находится вывод команды show
Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
    Interface
    IP-Address
    Status
    Protocol
Информация должна возвращаться в виде списка кортежей: [('FastEthernet0/0','10.0.1.1', 'up', 'up'),
('FastEthernet0/1', '10.0.2.1', 'up', 'up'), ('FastEthernet0/2', 'unassigned', 'up', 'up')]
"""
"""
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            15.0.15.1       YES manual up                    up
"""
import re


def parse_cdp(filename):
    regex = ('(?P<interface>\S+)\s+(?P<ipadd>\S+)\s+\S+\s\S+\s+(?P<status>\D{21})\s+(?P<protocol>\S+)')
    # разбор стороки 
    # (?P<interface>\S+)\s+           - имя интерфейса и проблы после него 
    # (?P<ipadd>\S+)\s+\S+\s\S+\s+    - IP_Address. пробелы полсе него колонка ОК? и прблел, колонока Method и пробел 
    # (?P<status>\D{21})\s+           - статус 21 символ кроме цифр ипробелы полсе него  
    result = []
    with open(filename) as f:
        for line in f:
            if 'show ip interface brief' in line:
                pass
            elif line.startswith('Interface'):
                pass
            else:
                tuple_temp=()
                temp_list=[]
                match = re.search(regex,line)
                Interface = match.group('interface')
                #print ('Interface ',  Interface)
                IP_Address = match.group('ipadd')
                #print ('IP-Address ', IP_Address)
                Status = match.group('status')
                #print ('Status ', Status)
                Protocol = match.group('protocol')
                #print ('Protocol ', Protocol)
                temp_list.append(Interface)
                temp_list.append(IP_Address)
                temp_list.append(Status)
                temp_list.append(Protocol)
                #print (temp_list)
                tuple_temp=tuple(temp_list)
                result.append(tuple_temp)
                
    return result
#################################################################################################
if __name__ == '__main__':
    result = []
    file_name = '/home/ubuntu/workspace/python/tasks/9_regular/9_4/sh_ip_int_br_2.txt'
    result = parse_cdp(file_name)
    print (result)
    #print('\n'.join(result))