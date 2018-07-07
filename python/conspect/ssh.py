#!/bin/python3
#----------------------------
# Program  by Konstantin. B.
#
# Version	Date		
# 1.0 		2018
# Info
#
#----------------------------
# Соединение с сервером SSH и выполнение команды
# в удаленной системе

#!/usr/bin/env python

import paramiko


hostname = "192.168.50.10"
port = 22
username = 'root'
password = 'Aa123456'
#pkey_file = '/home/jmjones/.ssh/id_rsa'                    # для авторизации по ключу
if __name__ == "__main__":
    #key = paramiko.RSAKey.from_private_key_file(pkey_file) # для авторизации по ключу
    #client.load_system_host_keys()                         # для авторизации по ключу
    paramiko.util.log_to_file('paramiko.log')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, username=username, password=password, port=port)
    #client.connect(hostname=hostname, port=port, pkey=key) # для авторизации по ключу
    stdin, stdout, stderr = client.exec_command('ls -l')
    data = stdout.read() + stderr.read()
    print (data)
    stdin, stdout, stderr = client.exec_command('ifconfig')
    print (stdout.read())

    client.close()
"""
b'total 4\n-rw-------. 1 root root 915 Mar  2  2016 anaconda-ks.cfg\ndrwxr-xr-x  3 root root 114 May 26 12:06 ansible\n-rw-r--r--  1 root root   0 May 19 15:55 astra.yml\n'
b'eno16777728: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n        inet 192.168.50.10  netmask 255.255.255.0  broadcast 192.168.50.255\n        inet6 fe80::20c:29ff:fe0d:704d  prefixlen 64  scopeid 0x20<link>\n        ether 00:0c:29:0d:70:4d  txqueuelen 1000  (Ethernet)\n        RX packets 182091  bytes 183651665 (175.1 MiB)\n        RX errors 0  dropped 0  overruns 0  frame 0\n        TX packets 113246  bytes 76615313 (73.0 MiB)\n        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0\n\neno33554952: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n        inet 192.168.10.1  netmask 255.255.255.0  broadcast 192.168.10.255\n        inet6 fe80::20c:29ff:fe0d:7057  prefixlen 64  scopeid 0x20<link>\n        ether 00:0c:29:0d:70:57  txqueuelen 1000  (Ethernet)\n        RX packets 91120  bytes 31268314 (29.8 MiB)\n        RX errors 0  dropped 0  overruns 0  frame 0\n        TX packets 159959  bytes 251087724 (239.4 MiB)\n        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0\n\nlo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536\n        inet 127.0.0.1  netmask 255.0.0.0\n        inet6 ::1  prefixlen 128  scopeid 0x10<host>\n        loop  txqueuelen 0  (Local Loopback)\n        RX packets 637  bytes 61899 (60.4 KiB)\n        RX errors 0  dropped 0  overruns 0  frame 0\n        TX packets 637  bytes 61899 (60.4 KiB)\n        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0\n\n'

