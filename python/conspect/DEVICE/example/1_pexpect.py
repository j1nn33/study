import pexpect
import getpass
import sys


COMMAND = sys.argv[1]                   # команда, которую нужно выполнить, передается как аргумент
USER = input('Username: ')              # запрашивается логин, пароль и пароль на режим enable
PASSWORD = getpass.getpass()            # пароли запрашиваются с помощью модуля getpass
ENABLE_PASS = getpass.getpass(prompt='Enter enable password: ')
                                        #  список IP-адресов устройств, к которым будет выполняться
DEVICES_IP = ['192.168.100.1','192.168.100.2','192.168.100.3']  

for IP in DEVICES_IP:
    print('Connection to device {}'.format(IP))
    #ыполняется подключение по SSH к текущему адресу, используя указанное имя пользователя
    with pexpect.spawn('ssh {}@{}'.format(USER, IP)) as ssh:
        # expect - ожидание подстроки
        # sendline - когда строка появилась, отправляется команда
        
        ssh.expect('Password:')
        ssh.sendline(PASSWORD)
        
        # Обратите внимание на строку ssh.expect('[#>]'). Метод expect ожидает не просто строку, а регулярное выражение.
        ssh.expect('[#>]')
        ssh.sendline('enable')

        ssh.expect('Password:')
        ssh.sendline(ENABLE_PASS)

        ssh.expect('#')
        ssh.sendline('terminal length 0')

        ssh.expect('#')
        ssh.sendline(COMMAND)

        ssh.expect('#')
        # before позволяет считать всё, что поймал pexpect до предыдущей подстроки в expect
        print(ssh.before.decode('utf-8'))



'''
Example:

$ python 1_pexpect.py 'sh ip int br'
Username: nata
Password:
Enter enable secret:
Connection to device 192.168.100.1
sh ip int br
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        192.168.100.1   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.1.10.1       YES manual up                    up
FastEthernet0/1.20     10.1.20.1       YES manual up                    up
FastEthernet0/1.30     10.1.30.1       YES manual up                    up
FastEthernet0/1.40     10.1.40.1       YES manual up                    up
FastEthernet0/1.50     10.1.50.1       YES manual up                    up
FastEthernet0/1.60     10.1.60.1       YES manual up                    up
FastEthernet0/1.70     10.1.70.1       YES manual up                    up
R1
Connection to device 192.168.100.2
sh ip int br
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        192.168.100.2   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.2.10.1       YES manual up                    up
FastEthernet0/1.20     10.2.20.1       YES manual up                    up
FastEthernet0/1.30     10.2.30.1       YES manual up                    up
FastEthernet0/1.40     10.2.40.1       YES manual up                    up
FastEthernet0/1.50     10.2.50.1       YES manual up                    up
FastEthernet0/1.60     10.2.60.1       YES manual up                    up
FastEthernet0/1.70     10.2.70.1       YES manual up                    up
R2
Connection to device 192.168.100.3
sh ip int br
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        192.168.100.3   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.3.10.1       YES manual up                    up
FastEthernet0/1.20     10.3.20.1       YES manual up                    up
FastEthernet0/1.30     10.3.30.1       YES manual up                    up
FastEthernet0/1.40     10.3.40.1       YES manual up                    up
FastEthernet0/1.50     10.3.50.1       YES manual up                    up
FastEthernet0/1.60     10.3.60.1       YES manual up                    up
FastEthernet0/1.70     10.3.70.1       YES manual up                    up
R3

'''
