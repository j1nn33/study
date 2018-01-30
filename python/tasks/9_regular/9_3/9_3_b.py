"""
Проверить работу функции parse_cfg из задания 9.3a на конфигурации config_r2.txt.
на интерфейсе e0/1 назначены два IP-адреса:
        interface Ethernet0/1
        ip address 10.255.2.2 255.255.255.0
        ip address 10.254.2.2 255.255.255.0 secondary
А в словаре, который возвращает функция parse_cfg, интерфейсу Ethernet0/1
соответствует только один из них (второй).

Переделайте функцию parse_cfg из задания 9.3a таким образом, чтобы она
возвращала список кортежей для каждого интерфейса. Если на интерфейсе назначен
только один адрес, в списке будет один кортеж. Если же на интерфейсе настроены
несколько IP-адресов, то в списке будет несколько кортежей.
Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.
Обратите внимание, что в данном случае, можно не проверять корректность IP-
адреса, диапазоны адресов и так далее, так как обрабатывается вывод команды, а не
ввод пользователя.
"""
import re


def regular(info_list):
    result = {}
    tuple_temp_1 = ()
    tuple_temp_2 = ()
    #print('\n'.join(info_list))
    print('#######################')
    for x in info_list:                           # проходим посторчно список, полученный из файла
        match_eth = re.search('interface \S+',x)  # поиск строк  с interface 
        if match_eth:
            eth=match_eth.group(0)                # запоминаем интерфейс (они могут не содержать IP , mask)
            #print (eth)
        match = re.search('(?P<ip>\d+.\d+.\d+.\d+)\s(?P<mask>\d+.\d+.\d+.\d+)', x)
        match_2 = re.search('(?P<ip>\d+.\d+.\d+.\d+)\s(?P<mask>\d+.\d+.\d+.\d+) secondary', x)    
        if match:                               
            print (eth)                           # здесь будет крайний нахденый интерфейс
            #print (match.group('ip'),' ',match.group('mask'))
            tuple_temp_1 = (match.group('ip'),match.group('mask'))
            print(tuple_temp_1)
            result[eth]=(tuple_temp_1,tuple_temp_2)
        if match_2:
            tuple_temp_2 = (match_2.group('ip'),match.group('mask'))
            print(tuple_temp_2)
            result[eth]=(tuple_temp_1,tuple_temp_2)
            tuple_temp_2 = ()                     # обнуляем второй ip чтобы он не задваивался на др интерфейсах
    return result


################################################################################################


def read_file(file_name):                         # открытие файла
    temp_list=[]    
    try:                                          # обработка исключения на наличие файла
        with open(file_name, 'r') as f:
            for line in f:
               temp_list.append(line.rstrip())    # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('---FUNCTION---No such file')
    return temp_list

#################################################################################################
if __name__ == '__main__':
    result = {}
    info_list = (read_file('/home/ubuntu/workspace/python/tasks/9_regular/9_3/config_r2.txt'))
    result = regular(info_list)
    print (result)
    #print('\n'.join(result))