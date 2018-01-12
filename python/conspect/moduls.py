# способы импорта модуля:
import module               # модуль в текущем пространстве имен. Их можно вызывать без имени модуля
import module as            # объекты модуля не попадают в именное пространство текущей программы

import module as os
os.getlogin()

from module import object   # Если в имени файла содержится точка

import subprocess as sp
sp.check_output('ping -c 2 -n 8.8.8.8', shell=True)
    # удобно использовать, когда из всего модуля нужны только одна-две функции:

from os import getlogin, getcwd
   
    # Теперь эти функции доступны в текущем именном пространстве
    
from module import *        # импортирует все имена модуля в текущее именное пространство 

from os import *


# Создание своих модулей

""" sw_int_templates.py
access_template = ['switchport mode access',
                   'switchport access vlan',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk allowed vlan']

l3int_template = ['no switchport', 'ip address']
"""
"""sw_data.py
sw1_fast_int = {
                'access':{
                         '0/12':'10',
                         '0/14':'11',
                         '0/16':'17'}}
"""
import sw_int_templates as sw_temp            # импорт всего файла sw_int_templates как sw_temp
                                              # вместо sw_int_templates.access_template можно sw_temp.access_template

from sw_data import sw1_fast_int              # - из модуля sw_data импортируется только  sw1_fast_int

def generate_access_cfg(sw_dict):
    result = []
    for intf, vlan in sw_dict['access'].items():
        result.append('interface FastEthernet' + intf)
        for command in sw_temp.access_template:
            if command.endswith('access vlan'):
                result.append(' {} {}'.format(command, vlan))
            else:
                result.append(' {}'.format(command))
    return result

print('\n'.join(generate_access_cfg(sw1_fast_int)))
####################################################################33

if __name__ == '__main__' 

# Переменная __name__ - это специальная переменная, которая выставляется равной
# "__main__" , если файл запускается как основная программа, и выставляется равной
# имени модуля, если модуль импортируется. Таким образом, условие 
if __name__ == '__main__'
# проверяет, был ли файл запущен напрямую.