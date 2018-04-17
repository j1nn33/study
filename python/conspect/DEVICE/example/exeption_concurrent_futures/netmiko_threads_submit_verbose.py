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
    all_results = {}
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_ssh = []
        for device in devices:
            future = executor.submit(function, device, command)
            future_ssh.append(future)
            print('Future: {} for device {}'.format(future, device['ip']))
        for f in as_completed(future_ssh):
            result = f.result()
            print('Future done {}'.format(f))
            all_results.update(result)
    return all_results


if __name__ == '__main__':
    devices = yaml.load(open('devices.yaml'))
    all_done = threads_conn(connect_ssh,
                            devices['routers'],
                            command='sh clock')
    pprint(all_done)

"""

Так как по умолчанию используется ограничение в два потока, только два из трех future
показывают статус running. Третий находится в состоянии pending и ждет, пока до него
дойдет очередь.



$ python netmiko_threads_submit_verbose.py
===> 06:16:56.059256 Connection to device: 192.168.100.1
Future: <Future at 0xb68427cc state=running> for device 192.168.100.1
===> 06:16:56.059434 Connection to device: 192.168.100.2
Future: <Future at 0xb68483ac state=running> for device 192.168.100.2
Future: <Future at 0xb6848b4c state=pending> for device 192.168.100.3
<=== 06:17:01.482761 Received result from device: 192.168.100.2
===> 06:17:01.589605 Connection to device: 192.168.100.3
Future done <Future at 0xb68483ac state=finished returned dict>
<=== 06:17:07.226815 Received result from device: 192.168.100.3
Future done <Future at 0xb6848b4c state=finished returned dict>
<=== 06:17:11.444831 Received result from device: 192.168.100.1
Future done <Future at 0xb68427cc state=finished returned dict>
{'192.168.100.1': '*06:17:11.273 UTC Mon Aug 28 2017',
'192.168.100.2': '*06:17:01.310 UTC Mon Aug 28 2017',
'192.168.100.3': '*06:17:07.055 UTC Mon Aug 28 2017'}

"""