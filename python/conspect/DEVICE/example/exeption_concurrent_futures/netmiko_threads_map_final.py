from concurrent.futures import ThreadPoolExecutor
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
    with ThreadPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices, repeat(command))
    return list(f_result)


if __name__ == '__main__':
    devices = yaml.load(open('devices.yaml'))
    all_done = threads_conn(connect_ssh,
                            devices['routers'],
                            command='sh clock')
    pprint(all_done)

"""
$ python netmiko_threads_map_final.py
===> 05:01:08.314962 Connection to device: 192.168.100.1
===> 05:01:08.315114 Connection to device: 192.168.100.2
<=== 05:01:13.693083 Received result from device: 192.168.100.2
===> 05:01:13.799002 Connection to device: 192.168.100.3
<=== 05:01:19.363250 Received result from device: 192.168.100.3
<=== 05:01:23.685859 Received result from device: 192.168.100.1
[{'192.168.100.1': '*05:01:23.513 UTC Mon Aug 28 2017'},
{'192.168.100.2': '*05:01:13.522 UTC Mon Aug 28 2017'},
{'192.168.100.3': '*05:01:19.189 UTC Mon Aug 28 2017'}]
"""