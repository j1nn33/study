#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
def send_show_command.
        - Функция подключается по SSH (с помощью netmiko) к устройствам из списка,
          и выполняет команду на основании переданных аргументов.

                Параметры функции:
                * devices_list - список словарей с параметрами подключения к устройствам, которым надо передать команды
                * command - команда, которую надо выполнить

                Функция возвращает словарь с результатами выполнения команды:
                * ключ - IP устройства
                * значение - результат выполнения команды
----

Переделать функцию send_show_command из задания 12.1 таким образом,
чтобы обрабатывалось исключение, которое генерируется
при ошибке аутентификации на устройстве.

При возникновении ошибки, должно выводиться сообщение исключения.

Дополнить функцию send_show_command из задания 12.1a таким образом,
чтобы обрабатывалось не только исключение, которое генерируется
при ошибке аутентификации на устройстве, но и исключение,
которое генерируется, когда IP-адрес устройства недоступен.

При возникновении ошибки, должно выводиться сообщение исключения.

'''
#import yaml
import os
import glob
import pprint
import netmiko
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException


command = 'sh ip int br'
yml_file = 'devices.yaml'


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


def connect_ssh(device_dict, commands):
    print ('FUNCTION connect_ssh IN PROGRESS')
    pprint.pprint(device_dict)

    
    # кусок кода не тестировался в виду отсутвия оборудования 
    try:
        with ConnectHandler(**device_dict) as ssh:      # Подключение по SSH  **device_dict - передача словаря
            ssh.enable()
    except netmiko.socket.error:
        print ('Connection error - ip is invalid')
    else:
        try:
        
            result_device = ssh.send_config_set(commands)    # отправить список команд
        except NetMikoAuthenticationException as e:
            print(e)
   
    return(result_device)

if __name__ == '__main__':
    
    device_dict=(get_device_list(yml_file))
    # цикл обхода значений ключа routers в словаре   
    for router in device_dict['routers']:
        connect_ssh(router, command)
    
    #print (send_show_command(devices_list, command))