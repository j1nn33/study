# функция check_ip_addresses, которая проверяет доступность IP-адресов.
# Функция ожидает как аргумент список IP-адресов. И возвращает два списка:
#        список доступных IP-адресов
#        список недоступных IP-адресов
# Для проверки доступности IP-адреса, используйте ping. Адрес считается доступным,
# если на три ICMP-запроса пришли три ответа.
import ipaddress
import subprocess

subnet = ipaddress.ip_network('192.168.40.0/29')  # создает объекты описывающие сеть

def ping_ip(ip_address):
    """
    ping хост 3 раз в если все 3 раза успешно, то возвращает 0
    """
    ip_address=str(ip_address)      # переводим в стороку тк subprocess.call хочет str
    if  subprocess.call (['ping','-c','3',ip_address]) ==0:
        return True
    else:
        return False

def check_ip_addresses(subnet):
    active_ip_list = []
    inactive_ip_list = []
    # active_ip_list = list(ip_list)
    #print (subnet.hosts)
    for ip in subnet:  # проход по адресам в подсети
        if ping_ip(ip) == True:
            active_ip_list.append(str(ip))
        else:
            inactive_ip_list.append(str(ip))

    return (active_ip_list, inactive_ip_list)


if __name__ == '__main__':
    a, b = check_ip_addresses(subnet)
    print('active IP ', '\n'.join(a))
    print('inactive IP ', '\n'.join(b))