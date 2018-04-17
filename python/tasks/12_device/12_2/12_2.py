#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
send_config_commands (devices_list, config_commands, output) 
    config_commands - список команд, которые надо выполнить
    который контролирует будет ли результат выполнения команд выводиться на стандартный поток вывода
return  dict_result
           dict_result  temp_dict[ip]=[result_device]
Задание 12.2a
"""
#import yaml
import os
import glob
import pprint
#import netmiko
#from netmiko import ConnectHandler
#from netmiko.ssh_exception import NetMikoAuthenticationException

output = True
yml_file = 'devices.yaml'
commands = ['logging 10.255.255.1',
            'logging buffered 20010',
            'no logging console']


def get_device_list(yml_file):
    print ('FUNCTION get_device_list IN PROGRESS')
    print ('yml_file ', yml_file)
    if os.path.exists(yml_file):
         print (yml_file,' - существует ')
         """  раскоментировать для работы с yaml
         with open(yml_file) as f:
            devices_list = yaml.load(f)
         pprint.pprint(devices_list)
         
         """
    else:
        print (yml_file,' - не существует ')
    
    devices_list = {'routers': [{'device_type': 'cisco_ios',
              'ip': '192.168.100.1',
              'password': 'cisco',
              'secret': 'cisco',
              'username': 'cisco'},
             {'device_type': 'cisco_ios',
              'ip': '192.168.100.2',
              'password': 'cisco',
              'secret': 'cisco',
              'username': 'cisco'},
             {'device_type': 'cisco_ios',
              'ip': '192.168.100.3',
              'password': 'cisco',
              'secret': 'cisco',
              'username': 'cisco'}]}
    return (devices_list)

def send_config_commands (devices_list, config_commands, output):
    print ('FUNCTION connect_ssh IN PROGRESS')
    #pprint.pprint(devices_list)

    """
    # кусок кода не тестировался в виду отсутвия оборудования 
    try:
        with ConnectHandler(**devices_list) as ssh:      # Подключение по SSH  **devices_list - передача словаря
            ssh.enable()
    except netmiko.socket.error:
        print ('Connection error - ip is invalid')
    else:
        try:
        
            result_device = ssh.send_config_set(config_commands)    # отправить список команд
        except NetMikoAuthenticationException as e:
            print(e)
    """
    # симуляция получения информации с устройсва и дальнейшая логика ее обработки
    value = {}
    dict_result = {}
    result_device = 'result_device'
    for key in devices_list.keys():
        for value in devices_list[key]:        
            ip = value['ip']
            temp_dict={}                      
            temp_dict[ip]=[result_device]
            dict_result.update(temp_dict)  
    if output is True:
        print(dict_result)
    return(dict_result)


if __name__ == '__main__':
    device_dict=(get_device_list(yml_file))
    #for router in device_dict['routers']:
    send_config_commands (device_dict, commands, output)
    