import paramiko
import getpass
import sys
import time

COMMAND = sys.argv[1]
USER = input('Username: ')
PASSWORD = getpass.getpass()
ENABLE_PASS = getpass.getpass(prompt='Enter enable password: ')

DEVICES_IP = ['192.168.100.1','192.168.100.2','192.168.100.3']

for IP in DEVICES_IP:
    print('Connection to device {}'.format( IP ))
    client = paramiko.SSHClient()     # представляет соединение к SSH-серверу. Он выполняет аутентификацию клиента.
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())    # устанавливает, какую политику использовать,
                                                                    # когда выполнятся подключение к серверу, ключ которого неизвестен.
                                                                    # paramiko.AutoAddPolicy() - политика, которая автоматически добавляет новое
                                                                    # имя хоста и ключ в локальный объект HostKeys.
    client.connect(hostname=IP, username=USER, password=PASSWORD,   # метод, который выполняет подключение к SSH-серверу и
                                                                    # аутентифицирует подключение
                   look_for_keys=False, allow_agent=False)          # по умолчанию paramiko выполняет аутентификацию по
                                                                    # ключам. Чтобы отключить это, надо поставить флаг в False
                                                                    # allow_agent - paramiko может подключаться к локальному SSH агенту
                                                                    # ОС. Это нужно при работе с ключами, а так как в данном случае
                                                                    # аутентификация выполняется по логину/паролю, это нужно отключить.
    with client.invoke_shell() as ssh:                              # после выполнения предыдущей команды уже есть подключение к серверу.
                                                                    # Метод invoke_shell позволяет установить интерактивную сессию SSH с сервером.
        # Внутри установленной сессии выполняются команды и получаются данные:
        ssh.send('enable\n')                        # - отправляет указанную строку в сессию
        ssh.send(ENABLE_PASS + '\n')                # - получает данные из сессии. В скобках указывается
        time.sleep(1)
        # с помощью неё указывается пауза - сколько времени подождать, прежде
        # чем скрипт продолжит выполняться. Это делается для того, чтобы
        # дождаться выполнения команды на оборудовании

        ssh.send('terminal length 0\n')
        time.sleep(1)
        ssh.recv(1000).decode('utf-8')

        ssh.send(COMMAND + '\n')
        time.sleep(2)
        result = ssh.recv(5000).decode('utf-8')
        print(result)



'''
Example:
$ python 3_paramiko.py
Username: cisco
Password:
Enter enable secret:
Connection to device 192.168.100.1

R1>enable
Password:
R1#terminal length 0


R1#
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
R1#
Connection to device 192.168.100.2

R2>enable
Password:
R2#terminal length 0
R2#
sh ip int br
FastEthernet0/0        192.168.100.2   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.2.10.1       YES manual up                    up
FastEthernet0/1.20     10.2.20.1       YES manual up                    up
FastEthernet0/1.30     10.2.30.1       YES manual up                    up
FastEthernet0/1.40     10.2.40.1       YES manual up                    up
FastEthernet0/1.50     10.2.50.1       YES manual up                    up
FastEthernet0/1.60     10.2.60.1       YES manual up                    up
FastEthernet0/1.70     10.2.70.1       YES manual up                    up
R2#
Connection to device 192.168.100.3

R3>enable
Password:
R3#terminal length 0
R3#
sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0        192.168.100.3   YES NVRAM  up                    up
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/1.10     10.3.10.1       YES manual up                    up
FastEthernet0/1.20     10.3.20.1       YES manual up                    up
FastEthernet0/1.30     10.3.30.1       YES manual up                    up
FastEthernet0/1.40     10.3.40.1       YES manual up                    up
FastEthernet0/1.50     10.3.50.1       YES manual up                    up
FastEthernet0/1.60     10.3.60.1       YES manual up                    up
FastEthernet0/1.70     10.3.70.1       YES manual up                    up
R3#

'''
