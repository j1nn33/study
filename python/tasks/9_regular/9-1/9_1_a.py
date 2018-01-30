# Создать скрипт, который будет ожидать два аргумента:
# 1. имя файла, в котором находится вывод команды show
# 2. регулярное выражение
# на стандартный поток вывода должны быть выведены те строки из файла,
# в которых было найдено совпадение с регулярным выражением.

import re

def regular(info_list, regular):
    result = []
    print('\n'.join(info_list))  
    print('#######################')
    regular1 = re.search('\S\S\S', regular).group()+' '
    regular2 = re.search('(\S+)\s+(\S+)', regular).group(2)+' '
    print ('regular1 ', regular1)
    print ('regular2 ', regular2)
    for x in info_list:                           # проходим посторчно список, полученный из файла
        match_str1 = re.search(regular1, x)       # поиск строк в файле которые соответсвуют регулярному выражению
        match_str2 = re.search(regular2, x)
        if match_str1:
            result.append(x)
        if match_str2:
            result.append(x)
          
    return result

def read_file(file_name):                         # открытие файла
    temp_list=[]    
    try:                                          # обработка исключения на наличие файла
        with open(file_name, 'r') as f:
            for line in f:
               temp_list.append(line.rstrip())    # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('---FUNCTION---No such file')
    return temp_list




if __name__ == '__main__':
    info_list = []
    result = []
    info_list = (read_file('/home/ubuntu/workspace/python/tasks/9_regular/9-1/sh_ip_int_br_switch.txt'))
    regular_str = "0/1, 0/3"
    result = regular(info_list,regular_str)
    print('\n'.join(result))  