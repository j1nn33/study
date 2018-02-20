from __future__ import print_function
from collections import namedtuple
import platform
import pwd
import argparse

print (platform.uname())
# uname_result(system='Linux', node='SUSE', release='4.4.92-31-default', version='#1 SMP Sun Oct 22 06:56:24 UTC 2017 (1d80e8a)', machine='x86_64', processor='x86_64')

print (platform.uname()[0])
# Linux

print (platform.linux_distribution())
# ('openSUSE ', '42.3', 'x86_64')


# вывод информации о процессоре
with open('/proc/cpuinfo') as f:
    for line in f:
        print(line.rstrip('\n'))

with open('/proc/cpuinfo') as f:
    for line in f:
        # Ignore the blank line separating the information between
        # details about two processing units
        if line.strip():
            if line.rstrip('\n').startswith('model name'):
                model_name = line.rstrip('\n').split(':')[1]
                print(model_name)

# число ЗАПУЩЕННЫХ ПРОЦЕССОВ

import os
def process_list():

    pids = []
    for subdir in os.listdir('/proc'):
        if subdir.isdigit():
            pids.append(subdir)

    return pids


if __name__=='__main__':

    pids = process_list()
    print('Total number of running processes:: {0}'.format(len(pids)))

# Total number of running processes:: 185



# Network Statistics

#from __future__ import print_function
#from collections import namedtuple

def netdevs():
    ''' RX and TX bytes for each of the network devices '''

    with open('/proc/net/dev') as f:
        net_dump = f.readlines()

    device_data={}
    data = namedtuple('data',['rx','tx'])
    for line in net_dump[2:]:
        line = line.split(':')
        if line[0].strip() != 'lo':
            device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0),
                                                float(line[1].split()[8])/(1024.0*1024.0))

    return device_data

if __name__=='__main__':

    netdevs = netdevs()
    for dev in netdevs.keys():
        print('{0}: {1} MiB {2} MiB'.format(dev, netdevs[dev].rx, netdevs[dev].tx))

# eth0: 60.76247787475586 MiB 2.7713022232055664 MiB
# br0: 57.78486442565918 MiB 2.7743377685546875 MiB

#!/usr/bin/env python

"""
Print all the users and their login shells
"""

#from __future__ import print_function
#import pwd


# Get the users from /etc/passwd
def getusers():
    users = pwd.getpwall()
    for user in users:
        print('{0}:{1}'.format(user.pw_name, user.pw_shell))

if __name__=='__main__':
    getusers()

"""
at:/bin/bash
avahi:/bin/false
avahi-autoipd:/bin/false
bin:/bin/bash
colord:/sbin/nologin
daemon:/bin/bash
dnsmasq:/bin/false
ftp:/bin/bash
games:/bin/bash
gdm:/bin/false
lp:/bin/bash
mail:/bin/false
man:/bin/bash
messagebus:/bin/false
news:/bin/bash
nm-openconnect:/sbin/nologin
nm-openvpn:/sbin/nologin
nobody:/bin/bash
nscd:/sbin/nologin
ntp:/bin/false
openslp:/sbin/nologin
polkitd:/sbin/nologin
postfix:/bin/false
pulse:/sbin/nologin
root:/bin/bash
rpc:/sbin/nologin
rtkit:/bin/false
srvGeoClue:/sbin/nologin
sshd:/bin/false
statd:/sbin/nologin
systemd-bus-proxy:/sbin/nologin
systemd-timesync:/sbin/nologin
tftp:/bin/false
uucp:/bin/bash
vnc:/sbin/nologin
wwwrun:/bin/false
const:/bin/bash
radvd:/sbin/nologin
qemu:/sbin/nologin
pesign:/bin/false
"""
