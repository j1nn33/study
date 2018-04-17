import sys
import yaml


from netmiko import ConnectHandler

#COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))   #  devices.yaml создан для подключения netmiko


def connect_ssh(device_dict, commands):

    print('Connection to device {}'.format( device_dict['ip'] ))

    with ConnectHandler(**device_dict) as ssh:     # Подключение по SSH  **device_dict - передача словаря
        ssh.enable()

        result = ssh.send_config_set(commands)
        print(result)


commands_to_send = ['logg 10.1.12.3', 'ip access-li ext TESST2', 'permit ip any any']

for router in devices['routers']:    
    connect_ssh(router, commands_to_send)


"""
$ time python netmiko_function.py "sh ip int br"
...
real 0m6.189s
user 0m0.336s
sys 0m0.080s

"""