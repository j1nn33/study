"""
Переделать функцию parse_cfg из задания 9.3 таким образом, чтобы она возвращала словарь:
ключ: имя интерфейса
значение: кортеж с двумя строками:
                IP-адрес
                маска
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}
"""

import re


def regular(info_list):
    result = {}
    tuple_temp = ()
    #print('\n'.join(info_list))
    print('#######################')
    for x in info_list:                           # проходим посторчно список, полученный из файла
        match_eth = re.search('interface \S+',x)  # поиск строк  с interface 
        if match_eth:
            eth=match_eth.group(0)                # запоминаем интерфейс (они могут не содержать IP , mask)
            #print (eth)
        match = re.search('(?P<ip>\d+.\d+.\d+.\d+)\s(?P<mask>\d+.\d+.\d+.\d+)', x)
        if match:                               
            print (eth)                           # здесь будет крайний нахденый интерфейс
            print (match.group('ip'),' ',match.group('mask'))
            tuple_temp = (match.group('ip'),match.group('mask'))
            result[eth]=(tuple_temp)
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
    info_list = (read_file('/home/ubuntu/workspace/python/tasks/9_regular/9_3/config_r1.txt'))
    result = regular(info_list)
    print (result)
    #print('\n'.join(result))