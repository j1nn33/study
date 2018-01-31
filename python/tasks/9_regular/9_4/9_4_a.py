# Создать функцию convert_to_dict, которая ожидает два аргумента:
#     список с названиями полей
#     список кортежей с результатами отработки функции parse_sh_ip_int_br из задания 9.4
"""
Функция возвращает результат в виде списка словарей (порядок полей может быть
другой): [{'interface': 'FastEthernet0/0', 'status': 'up', 'protocol': 'up', 'address': '10.0.1.1'},
{'interface': 'FastEthernet0/1', 'status': 'up', 'protocol': 'up', 'address': '10.0.2.1'}]
"""
# первый аргумент - список headers
# второй аргумент - результат, который возвращает функции parse_show из прошлого задания
# Функцию parse_sh_ip_int_br не нужно копировать. Надо импортировать или саму
# функцию, и использовать то же регулярное выражение, что и в задании 9.4, или
# импортировать результат выполнения функции parse_show.
"""
 headers = ['interface', 'address', 'status', 'protocol']
"""
from parse_show import* 


headers = ['interface', 'address', 'status', 'protocol']
def convert_to_dict(headers, parse_show):
    result = []
    print ('#################')
    for j in parse_show:        # проходим по элементам (состоящих из списков) parse_show
        temp_dict = {}
        for i in range(0,4):
            temp_dict[headers[i]] = j[i]
        result.append(temp_dict)
    print ('#################')
    
    
    return result
#################################################################################################
if __name__ == '__main__':
    result = []
    temp_parse =()
    file_name = '/home/ubuntu/workspace/python/tasks/9_regular/9_4/sh_ip_int_br_2.txt'
    temp_parse = parse_cdp(file_name)
    result = convert_to_dict (headers, temp_parse)
    print (result)