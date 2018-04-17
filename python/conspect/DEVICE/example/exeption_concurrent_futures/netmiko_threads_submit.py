from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from datetime import datetime
import time
from itertools import repeat

import yaml
from netmiko import ConnectHandler


start_msg = '===> {} Connection to device: {}'
received_msg = '<=== {} Received result from device: {}'


def connect_ssh(device_dict, command):
    print(start_msg.format(datetime.now().time(), device_dict['ip']))
    if device_dict['ip'] == '192.168.100.1':
        time.sleep(10)
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        print(received_msg.format(datetime.now().time(), device_dict['ip']))
    return {device_dict['ip']: result}


def threads_conn(function, devices, limit=2, command=''):
    """
    блоке with два цикла:
    future_ssh - это список объектов future, который создается с помощью list
    comprehensions
    для создания future используется функция submit
    ей как аргументы передаются: имя функции, которую надо выполнить, и ее
    аргументы
    следующий цикл проходится по списку future с помощью функции as_completed.
    Эта функция возвращает future только когда они завершили работу или были
    отменены. При этом future возвращаются по мере завершения работы
    """
    all_results = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_ssh = [executor.submit(function, device, command)
                      for device in devices]
        for f in as_completed(future_ssh):
            all_results.append(f.result())
    return all_results


if __name__ == '__main__':
    devices = yaml.load(open('devices.yaml'))
    all_done = threads_conn(connect_ssh,
                            devices['routers'],
                            command='sh clock')
    pprint(all_done)

"""
$ python netmiko_threads_submit.py
===> 06:02:14.582011 Connection to device: 192.168.100.1
===> 06:02:14.582155 Connection to device: 192.168.100.2
<=== 06:02:20.155865 Received result from device: 192.168.100.2
===> 06:02:20.262584 Connection to device: 192.168.100.3
<=== 06:02:25.864270 Received result from device: 192.168.100.3
<=== 06:02:29.962225 Received result from device: 192.168.100.1
[{'192.168.100.2': '*06:02:19.983 UTC Mon Aug 28 2017'},
{'192.168.100.3': '*06:02:25.691 UTC Mon Aug 28 2017'},
{'192.168.100.1': '*06:02:29.789 UTC Mon Aug 28 2017'}]
"""