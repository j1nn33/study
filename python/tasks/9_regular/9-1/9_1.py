# Создать скрипт, который будет ожидать два аргумента:
# 1. имя файла, в котором находится вывод команды show
# 2. регулярное выражение
# на стандартный поток вывода должны быть выведены те строки из файла,
# в которых было найдено совпадение с регулярным выражением.

import re

def regular(info_list, regular):
    #print ('in function')
    result = []
    #print (info_list)
    print('\n'.join(info_list))  
    print('#######################')
    #print('regular ',type(regular),regular)
    for x in info_list:           # проходим посторчно список, полученный из файла
        #print('x ',type(x),x)
        match_str = re.search(regular, x)       # поиск строк в файле которые соответсвуют регулярному выражению
        #print(re.search(regular, x).group())
        #print (  match_str.group())
        if match_str:
            result.append(x)#.groupdict())
    
    
    #print (result)
    return result

def read_file(file_name):                                   # открытие файла
    temp_list=[]    
    try:                                                    # обработка исключения на наличие файла
        with open(file_name, 'r') as f:
            for line in f:
               temp_list.append(line.rstrip())              # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('---FUNCTION---No such file')
    return temp_list




if __name__ == '__main__':
    info_list = []
    result = []
    info_list = (read_file('/home/ubuntu/workspace/python/tasks/9_regular/9-1/sh_ip_int_br.txt'))
    #print(info_list)
    #regular_str = "Fas" 
    #regular_str = "manual"
    regular_str = "up +up"
    #regular_str = "up +up"
    #regular(info_list,regular_str)
    #print (regular(info_list,regular_str))
    result = regular(info_list,regular_str)
    #print (result)
    print('\n'.join(result))  