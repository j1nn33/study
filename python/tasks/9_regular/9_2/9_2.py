# Создать функцию return_match, которая ожидает два аргумента:
# имя файла, в котором находится вывод команды show sh_ip_int_br.txt
# регулярное выражение
# Функция должна обрабатывать вывод команды show построчно и возвращать список
# подстрок, которые совпали с регулярным выражением (не всю строку, где было
# найдено совпадение, а только ту подстроку, которая совпала с выражением).
# Вывести список всех IP-адресов из вывода команды.
#      Соответственно, регулярное выражение должно описывать подстроку с IP-адресом (то
#      есть, совпадением должен быть IP-адрес).
#   что в данном случае, мы можем не проверять корректность IP-адреса, диапазоны адресов 
#   и так далее, так как мы обрабатываем вывод команды, а не ввод пользователя

import re


def regular(info_list, regular):
    result = []
    print('\n'.join(info_list))
    #print (regular)
    print('#######################')
    for x in info_list:                           # проходим посторчно список, полученный из файла
        match = re.search(regular, x)
        if match:
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
    info_list = (read_file('/home/ubuntu/workspace/python/tasks/9_regular/9_2/sh_ip_int_br.txt'))
    regular_str = '\d+.\d+.\d+.\d+'
    result = regular(info_list,regular_str)
    print('\n'.join(result))  