# Делает тоже что и  parse_sh_cdp_neighbors_detail_ver1.py
import re
from pprint import pprint


def parse_cdp(filename):
    regex = ('Device ID: (?P<device>\S+)'                   # (?P<name>regex)
             '|IP address: (?P<ip>\S+)'                     # 
             '|Platform: (?P<platform>\S+ \S+),'            #
             '|Cisco IOS Software, (?P<ios>.+), RELEASE')   #

    result = {}

    with open('sh_cdp_neighbors_sw1.txt') as f:
        for line in f:
            match = re.search(regex, line)
            if match:
                if match.lastgroup == 'device':     # имя последней группы совпадеиня            
                    device = match.group(match.lastgroup)
                    result[device] = {}
                elif device:
                    result[device][match.lastgroup] = match.group(match.lastgroup)

    return result

pprint(parse_cdp('/home/ubuntu/workspace/python/conspect/example_book/regular/sh_cdp_neighbors_sw1.txt'))

