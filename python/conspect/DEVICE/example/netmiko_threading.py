import sys
import yaml
import threading

from netmiko import ConnectHandler


COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))


def connect_ssh(device_dict, command):
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)

        print('Connection to device {}'.format( device_dict['ip'] ))
        print(result)


def conn_threads(function, devices, command):
    threads = []
    for device in devices:
        # threading.Thread - класс, который создает поток
        # ему передается функция, которую надо выполнить, и её аргументы
        th = threading.Thread(target = function, args = (device, command))    
        th.start()               # запуск потока
        threads.append(th)       # поток добавляется в список

    for th in threads:
        th.join()                # метод ожидает завершения работы потока


conn_threads(connect_ssh, devices['routers'], COMMAND)

"""
$ time python netmiko_function_threading.py "sh ip int br"
...
real 0m2.229s
user 0m0.408s
sys 0m0.068s


Комментарии к функции conn_threads:
    threading.Thread - класс, который создает поток
                       ему передается функция, которую надо выполнить, и её аргументы
    th.start() - запуск потока
    threads.append(th) - поток добавляется в список
    th.join() - метод ожидает завершения работы потока
                метод join выполняется для каждого потока в списке. Таким образом, основная
                программа завершится, только когда завершат работу все потоки
                по умолчанию join ждет завершения работы потока бесконечно. Но можно
                ограничить время ожидания, передав join время в секундах. В таком случае
                join завершится после указанного количества секунд.


"""
