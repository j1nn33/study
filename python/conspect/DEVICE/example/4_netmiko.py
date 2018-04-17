import getpass
import sys

from netmiko import ConnectHandler


COMMAND = sys.argv[1]
USER = input('Username: ')
PASSWORD = getpass.getpass()
ENABLE_PASS = getpass.getpass(prompt='Enter enable password: ')

DEVICES_IP = ['192.168.100.1','192.168.100.2','192.168.100.3']


for IP in DEVICES_IP:
    print('Connection to device {}'.format(IP))
    DEVICE_PARAMS = {'device_type': 'cisco_ios',       # это словарь, в котором указываются параметры устройства
                     'ip': IP,                         # device_type - это предопределенные значения, которые понимает netmiko
                     'cisco_ios'                       # в данном случае, так как подключение выполняется к устройству с Cisco
                     'username': USER,                 # IOS, используется значение
                     'password': PASSWORD,
                     'secret': ENABLE_PASS}

    with ConnectHandler(**DEVICE_PARAMS) as ssh:      # танавливается соединение с
                                                      # устройством на основе параметров, которые находятся в словаре
                                                      # две звездочки перед словарем - это распаковка словаря
        ssh.enable()                                  #  переход в режим enable пароль передается автоматически
                                                      # используется значение ключа secret, который указан в словаре DEVICE_PARAMS
        result = ssh.send_command(COMMAND)            # отправка команды и получение вывода
        print(result)




'''
Examples:
$ python 4_netmiko.py
Username: cisco
Password:
Enter enable password:
Connection to device 192.168.100.1
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        192.168.100.1   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.1.10.1       YES manual up                    up
FastEthernet0/1.20     10.1.20.1       YES manual up                    up
FastEthernet0/1.30     10.1.30.1       YES manual up                    up
FastEthernet0/1.40     10.1.40.1       YES manual up                    up
FastEthernet0/1.50     10.1.50.1       YES manual up                    up
FastEthernet0/1.60     10.1.60.1       YES manual up                    up
FastEthernet0/1.70     10.1.70.1       YES manual up                    up
Connection to device 192.168.100.2
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        192.168.100.2   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.2.10.1       YES manual up                    up
FastEthernet0/1.20     10.2.20.1       YES manual up                    up
FastEthernet0/1.30     10.2.30.1       YES manual up                    up
FastEthernet0/1.40     10.2.40.1       YES manual up                    up
FastEthernet0/1.50     10.2.50.1       YES manual up                    up
FastEthernet0/1.60     10.2.60.1       YES manual up                    up
FastEthernet0/1.70     10.2.70.1       YES manual up                    up
Connection to device 192.168.100.3
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        192.168.100.3   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.3.10.1       YES manual up                    up
FastEthernet0/1.20     10.3.20.1       YES manual up                    up
FastEthernet0/1.30     10.3.30.1       YES manual up                    up
FastEthernet0/1.40     10.3.40.1       YES manual up                    up
FastEthernet0/1.50     10.3.50.1       YES manual up                    up
FastEthernet0/1.60     10.3.60.1       YES manual up                    up
FastEthernet0/1.70     10.3.70.1       YES manual up                    up
'''

