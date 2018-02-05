# С помощью функции draw_topology из файла draw_network_graph.py сгенерировать
# топологию, которая соответствует описанию в файле topology.yaml
# Обратите внимание на то, какой формат данных ожидает функция draw_topology.
# Описание топологии из файла topology.yaml нужно преобразовать соответствующим
# образом, чтобы использовать функцию draw_topology.
# В итоге, должно быть сгенерировано изображение топологии.
# Переделать функциональность скрипта из задания 10.2a, в функцию generate_topology_from_cdp.
# Функция generate_topology_from_cdp должна быть создана с параметрами:
#       list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
#       save_to_file - этот параметр управляет тем, будет ли записан в файл topology.yaml, итоговый словарь
#                                                   значение по умолчанию - True
#      топология сохраняется только, если аргумент save_to_file указан равным True
# Функция возвращает словарь, который описывает топологию. Словарь должен быть в том же формате, что и в задании 10.2a.


# С помощью функции parse_sh_cdp_neighbors из задания 10.2, обработать вывод  команды sh cdp neighbor из файлов:
# Объединить все словари, которые возвращает функция parse_sh_cdp_neighbors, в
# один словарь topology и записать его содержимое в файл topology.yaml.
#  Структура словаря topology должна быть такой:
#            {'R4': {'Fa0/1': {'R5': 'Fa0/1'},
#                    'Fa0/2': {'R6': 'Fa0/0'}},
#             'R5': {'Fa0/1': {'R4': 'Fa0/1'}},
#             'R6': {'Fa0/0': {'R4': 'Fa0/2'}}}

import glob
import re
import os
#import yaml
#import draw_network_graph
# from draw_network_graph import draw_topology


#################################################################################################
# читает файлы и передает результат в виде списка
def read_file(file_name):
    temp_list = []
    try:  # обработка исключения на наличие файла
        with open(file_name, 'r') as f:
            for line in f:
                temp_list.append(
                    line.rstrip())  # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('---FUNCTION---No such file')
    return temp_list


#################################################################################################
# парсим файл по строчно (получаем его как список строк)
def parse_sh_cdp_neighbors(out_file):
    dict_draw = {}
    dict_draw_temp = {}
    # цикл необходим тк в некоторых файлах сверх есть пустая строка
    # логика цикла ищем совпадение (служебный вывод либо None )
    # если служебный вывод то получаем из строки либо индекс строки либо индекс того чего ищем
    for line_in_file in out_file:
        posit = re.search('[>]', line_in_file)  # выражение для поиска >
        if posit:  # если совпадеине найдено
            posit = re.search('[>]', line_in_file).start()  # получаем позицию >
            my_name = line_in_file[:posit:]  # получаем имя устройсва до >

    for line_in_file in out_file:
        end_of_header_line = re.match('Device ID\s+', line_in_file)  # ищем нижню строчку шапки файла
        if end_of_header_line:  # если совпадеине найдено
            end_of_header_line = re.match('Device ID\s+', line_in_file).group()
            index_header = out_file.index(line_in_file)  # получаем индек этой строки в списк е out_file

    for line_in_file in out_file[index_header + 1::]:
        # R1           Eth 0/1         122           R S I           2811       Eth 0/0
        match = re.search('(?P<neighbors_name>\S+)\s+(?P<my_int>\S+\s\S+).+?(?P<neighbors_int>[Eth]\S+\s\d+\S\d+)',line_in_file)
        #  'R5': {'Fa0/1': {'R4': 'Fa0/1'}}
        my_int = match.group('my_int')
        neighbors_name = match.group('neighbors_name')
        neighbors_int = match.group('neighbors_int')
        # собираем для dict_for_draw
        #                {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
        #                 ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}
        # соответствует топологии:
        # [ R5 ]-Eth0/1 --- Eth0/1-[ R4 ]-Eth0/2---Eth0/0-[ R6 ]
        draw_temp1 = {}
        draw_temp2 = {}
        list_draw_temp1 = []
        list_draw_temp2 = []
        list_draw_temp1 = [my_name, my_int]
        list_draw_temp2 = [neighbors_name, neighbors_int]
        draw_temp1 = tuple (list_draw_temp1)
        draw_temp2 = tuple (list_draw_temp2)
        dict_draw_temp[draw_temp1]= draw_temp2
    dict_draw.update(dict_draw_temp)
    return dict_draw 

#################################################################################################
if __name__ == '__main__':
    directory = os.getcwd() + '/'  # /home/ubuntu/workspace/python/tasks/10_type_files/10_2/
    sh_cdp_n_files = glob.glob('sh_cd*')  # список имен файлов
    full_name_list_of_file = []
    list_in_file = []
    dict_total = {}
    #dict_for_draw = {}
    dict_device={}

    for file_name in sh_cdp_n_files:
        full_name = directory + file_name
        full_name_list_of_file.append(full_name)
    for file_name in full_name_list_of_file:
        list_of_file = read_file(file_name)
        dict_device = parse_sh_cdp_neighbors(list_of_file)
        # удаление задвоенных связей см topology_duble.svg
        for dic_device_item in dict_device:
            print (dic_device_item)
            print (dict_device[dic_device_item])
            if dict_device[dic_device_item] in dict_total:
                print ('pass')
            else:
                val={}
                val[dic_device_item]= dict_device[dic_device_item]
                dict_total.update(val)
    print ('DRAWING TOPOLOGY')
    #draw_network_graph.draw_topology(dict_total) 
   