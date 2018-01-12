import subprocess
from tempfile import TemporaryFile

import argparse


def ping_ip(ip_address, count=3):
    '''
    Ping IP address and return tuple:
    On success: (return code = 0, command output)
    On failure: (return code, error output (stderr))
    '''
    with TemporaryFile() as temp:
        try:
            output = subprocess.check_output(['ping', '-c', str(count), '-n', ip_address],
                                             stderr=temp)
            return 0, output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            temp.seek(0)
            return e.returncode, temp.read().decode('utf-8')


parser = argparse.ArgumentParser(description='Ping script')

parser.add_argument('host', action='store', help='IP or name to ping')
parser.add_argument('-c', action='store', dest='count', default=2, type=int,
                    help='Number of packets')

args = parser.parse_args()
print(args)

rc, message = ping_ip( args.host, args.count )
print(message)


"""
вместо указания опции -a , можно просто передать IP-адрес.
Он будет автоматически сохранен в переменной host .
И автоматически считается обязательным.
То есть, теперь не нужно указывать required=True и dest="ip" .
Кроме того, в скрипте указаны сообщения, которые будут выводиться при вызове help.
вызов скрипта выглядит так:


$ python ping_function_ver2.py 8.8.8.8 -c 2
Namespace(host='8.8.8.8', count=2)
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=49.203 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=51.764 ms
--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 49.203/50.484/51.764/1.280 ms


А сообщение help так:
$ python ping_function_ver2.py -h
usage: ping_function_ver2.py [-h] [-c COUNT] host
Ping script
positional arguments:
host IP or name to ping
optional arguments:
-h, --help show this help message and exit
-c COUNT Number of packets

"""