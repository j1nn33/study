import re
"""
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            15.0.15.1       YES manual up                    up
FastEthernet0/1            10.0.12.1       YES manual up                    up
FastEthernet0/2            10.0.13.1       YES manual up                    up
FastEthernet0/3            unassigned      YES unset  administratively down down
Loopback0                  10.1.1.1        YES manual up                    up
Loopback100                100.0.0.1       YES manual up                    up

"""
#line ='FastEthernet0/3            unassigned      YES unset  administratively down down'
#line = 'FastEthernet0/2            10.0.13.1       YES manual up                    up'
#line = 'R1#show ip interface brief'
line = 'Interface                  IP-Address      OK? Method Status                Protocol'


#regex = ('(?P<interface>\S+)\s+(?P<ipadd>\S+)\s+\S+\s\S+\s(?P<status>\S+)\s+(?P<protocol>\S+)')
#regex = ('(?P<interface>\S+)\s+(?P<ipadd>\S+)\s+\S+\s\S+\s+(?P<status>\S+\s\S+)\s+(?P<protocol>\S+)')
regex = ('(?P<interface>\S+)\s+(?P<ipadd>\S+)\s+\S+\s\S+\s+(?P<status>\D{21})\s+(?P<protocol>\S+)')

# разбор стороки 
# (?P<interface>\S+)\s+           - имя интерфейса и проблы после него 
# (?P<ipadd>\S+)\s+\S+\s\S+\s+    - IP_Address. пробелы полсе него колонка ОК? и прблел, колонока Method и пробел 
# (?P<status>\D{21})\s+           - статус 21 символ кроме цифр ипробелы полсе него  


match = re.search(regex,line)

Interface = match.group('interface')
print ('Interface ',  Interface)
IP_Address = match.group('ipadd')
print ('IP-Address ', IP_Address)
Status = match.group('status')
print ('Status ', Status)
Protocol = match.group('protocol')
print ('Protocol ', Protocol)