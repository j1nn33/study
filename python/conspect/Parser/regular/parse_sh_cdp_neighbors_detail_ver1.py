"""парсинг файла 
Задача получить такие поля:
имя соседа (Device ID: SW2)
IP-адрес соседа (IP address: 10.1.1.2)
платформу соседа (Platform: cisco WS-C2960-8TC-L)
версию IOS (Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version
12.2(55)SE9, RELEASE SOFTWARE (fc1))
И, для удобства, надо получить данные в виде словаря
"""
import re
from pprint import pprint
"""
{'R1': {'ios': '3800 Software (C3825-ADVENTERPRISEK9-M), Version 12.4(24)T1',
        'ip': '10.1.1.1',
        'platform': 'Cisco 3825'},
 'R2': {'ios': '2900 Software (C3825-ADVENTERPRISEK9-M), Version 15.2(2)T1',
        'ip': '10.2.2.2',
        'platform': 'Cisco 2911'},
 'SW2': {'ios': 'C2960 Software (C2960-LANBASEK9-M), Version 12.2(55)SE9',
         'ip': '10.1.1.2',
         'platform': 'cisco WS-C2960-8TC-L'}}
"""

def parse_cdp(filename):
    result = {}

    with open(filename) as f:
        for line in f:
            if line.startswith('Device ID'):
                neighbor = re.search('Device ID: (\S+)', line).group(1) # Первое совпадение строки Device ID: (\S+)
                # group - удаляет тех. вывод
                # group(0 ) - Device ID: SW2
                neighbor = re.search('Device ID: (\S+)', line).group(0)
                print(neighbor)
                result[neighbor] = {}
            elif line.startswith('  IP address'):
                ip = re.search('IP address: (\S+)', line).group(1)
                result[neighbor]['ip'] = ip
            elif line.startswith('Platform'):
                platform = re.search('Platform: (\S+ \S+),', line).group(1)
                result[neighbor]['platform'] = platform
            elif line.startswith('Cisco IOS Software'):
                ios = re.search('Cisco IOS Software, (.+), RELEASE', line).group(1)
                result[neighbor]['ios'] = ios

    return result

pprint(parse_cdp('/home/ubuntu/workspace/python/conspect/example_book/regular/sh_cdp_neighbors_sw1.txt'))
